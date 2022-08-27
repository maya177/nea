from gettext import npgettext
import json
from operator import truediv
from flask import Flask,request,render_template,session,url_for,redirect,jsonify
from flask_session import Session
from tempfile import mkdtemp
import hashlib
import sqlite3
import re
import librosa
import soundfile as sf
import json
import numpy as np
from datetime import datetime
from flask_mail import Mail, Message

now = datetime.now()
app = Flask(__name__)

#https://stackoverflow.com/questions/6332577/send-outlook-email-via-python
#https://stackoverflow.com/questions/37058567/configure-flask-mail-to-use-gmail
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mayaNbridgman@gmail.com'
EMAIL_HOST_PASSWORD = 'lboesehsgspqsxny'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False 

mail = Mail(app)


# stores session in temp directory on flask server instead of in a cookie
app.config["SESSION_FILE_DIR" ]= mkdtemp()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#begin session
app.config.from_object(__name__)
Session(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#user redirects instead of render template as it re requests form i think
@app.route('/',methods=['POST','GET'])
def signup():

    # if user is currently logged in
    if request.method=='POST':
        session.clear()
        conn = get_db_connection()
        #instead of just request.form
        #request.form.get[x, False] removes the assumption that it will always be part of the request
        #also use () instead of [] because .get is a method
        email = request.form.get("email", False)
        firstName = request.form.get("firstName", False)
        lastName = request.form.get("lastName", False)
        passwrd = request.form.get("password", False)


        if not email:
            return("Please enter an email")
        elif not firstName:
            return("Please enter a first name")
        elif not lastName:
            return("Please enter a last name")
        elif not passwrd:
            return("Please enter a password")
        
        if not re.search("^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{7,}$", passwrd):
            return("Please enter a password that is over 7 characters, has upper and lower case letters, a number, and a special character")
        
        passwrd =  hashlib.md5(passwrd.encode())
        if not re.search("[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):
            return("Please enter a valid email address")
        
        try:
            conn.execute("INSERT INTO students (firstName,lastName,email,passwrd) VALUES(?,?,?,?)",(firstName,lastName,email,passwrd.hexdigest()))
            conn.commit()
            conn.close()

        except sqlite3.IntegrityError:
            return("Email already in the system")
        
        #set user session
        session["email"] = email
        session["firstName"] = firstName
        session["lastName"] = lastName
        
        print("email before render" + email)
        return redirect(url_for("addTeachers"))

    return render_template("signup.html")

@app.route('/addTeachers', methods=['POST','GET'])
def addTeachers():
    print("add teachers working")
    if request.method=='POST':
        print("getting data")

        conn = get_db_connection()
        im_dict = request.form
        print(im_dict)
        #multi dictionary when multi field form
        #so using im_dict[i] will not work
        for i in range(len(im_dict)):
            if i%2 == 0:
                print(i)
                teacherName = im_dict[str(i)]
                teacherEmail = im_dict[str(i+1)]
                conn.execute("INSERT INTO teachers (teacherEmail,teacherName) VALUES(?,?)",(teacherEmail,teacherName))

                session["email"] = "su@subridgman.com"
                try:
                    studentEmail = session["email"]
                    conn.execute("INSERT INTO relationships (studentEmail,teacherEmail) VALUES(?,?)",(studentEmail,teacherEmail))
                    conn.commit()
                except:
                   return("please log in")
        conn.close()
                
        return redirect(url_for("home"))

    return render_template("addTeachers.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        session.clear()

        conn = get_db_connection()
        cur = conn.cursor()

        email = request.form.get("email", False)
        passwrd = hashlib.md5(request.form.get("password").encode())

        if not email:
            return("please enter an email")
        elif not passwrd:
            return("please enter a passwrd")

        cur.execute("SELECT email, passwrd, firstName, lastName FROM students where email = (?)", [email])
        studentrow = cur.fetchone()
        conn.close()

        print(email)
        print(studentrow[2])
        print(studentrow[3])

        try:
            if passwrd.hexdigest() == studentrow[1]:
                print("passwords match")
                session["email"] = email
                session["firstName"] = studentrow[2]
                session["lastName"] = studentrow[3]
                print("working")
                return render_template("home.html")
            else:
                return("incorrect password")
        except:
           return("this account does not exist")
       
    return render_template("login.html")
            
@app.route("/logout")
def logout():
    session["email"] = None
    session["firstName"] = None
    session["lastName"] = None
    return redirect("/login")

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/recorder", methods=['GET','POST'])
def recorder():
    if request.method == 'POST':
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M")
        f = open(f'./static/recordings/{filename}.wav', 'wb')
        f.write(request.data)
        f.close()
        x, fs = librosa.load(f'./static/recordings/{filename}.wav')

        session["x"] = x
        session["fs"] = fs

        response = jsonify("File received and saved!")
        return response

    
    return render_template("recorder.html")

@app.route("/threshold1", methods=['GET','POST'])
def threshold1():    
    #literally spent 1.5 hrs figuring out that ajax doesn't do normal redirects, had to implement success function in js that one tutorial lied
    if request.method == 'POST':
        try:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except:
            return "Error"
    return render_template("threshold1.html")
   
@app.route("/threshold2", methods=['GET','POST'])
def threshold2():
    if request.method == 'POST':
        try:
           #json_load()
            #request.json['data']

            data = request.get_json()
            path = data['src']
            #x is audio points, fs is sample rate
            t_x, t_fs = librosa.load(path)

            #zero crossing rate
            zcrs = librosa.feature.zero_crossing_rate(t_x).mean()
            #central spectroid
            cent = librosa.feature.spectral_centroid(y=t_x, sr=t_fs).mean()
            #mel scale converted freq
            mel = 2595.0 * np.log10(1.0 + t_fs / 700.0)

            ##loudness in rms
            # Compute the spectrogram (magnitude)
            n_fft = 2048
            hop_length = 1024
            spec_mag = abs(librosa.stft(t_x, n_fft=n_fft, hop_length=hop_length))
            # Convert the spectrogram into dB
            spec_db = librosa.amplitude_to_db(spec_mag)
            # Compute A-weighting values
            freqs = librosa.fft_frequencies(sr=t_fs, n_fft=n_fft)
            a_weights = librosa.A_weighting(freqs)
            a_weights = np.expand_dims(a_weights, axis=1)
            # Apply the A-weghting to the spectrogram in dB
            spec_dba = spec_db + a_weights
            # Compute the "loudness" value
            loudness = librosa.feature.rms(S=librosa.db_to_amplitude(spec_dba)).mean()

            print(zcrs)
            print(cent)
            print(mel)
            print(loudness)

            #need to scale them here and multiply by scale factors

            totalThreshold = 1
            conn = get_db_connection()
            session["email"] = "su@subridgman.com"
            studentEmail = session["email"]
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

            conn.execute("INSERT INTO thresholds (studentEmail,recordTime,zcrs,cent,mel,loudness,totalThreshold) VALUES(?,?,?,?,?,?,?)",(studentEmail,date_time,zcrs,cent,mel,loudness,totalThreshold))
            conn.commit()
            conn.close()

            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except ValueError:
            return "Error" 
    else:
        return render_template("threshold2.html")

@app.route('/compare', methods = ['GET','POST'])
def compare():
    x = session["x"]
    fs = session["fs"]

    #zero crossing rate
    zcrs = librosa.feature.zero_crossing_rate(x).mean()
    #central spectroid
    cent = librosa.feature.spectral_centroid(y=x, sr=fs).mean()
    #mel scale converted freq
    mel = 2595.0 * np.log10(1.0 + fs / 700.0)

    ##loudness in rms
    # Compute the spectrogram (magnitude)
    n_fft = 2048
    hop_length = 1024
    spec_mag = abs(librosa.stft(x, n_fft=n_fft, hop_length=hop_length))
    # Convert the spectrogram into dB
    spec_db = librosa.amplitude_to_db(spec_mag)
    # Compute A-weighting values
    freqs = librosa.fft_frequencies(sr=fs, n_fft=n_fft)
    a_weights = librosa.A_weighting(freqs)
    a_weights = np.expand_dims(a_weights, axis=1)
    # Apply the A-weghting to the spectrogram in dB
    spec_dba = spec_db + a_weights
    # Compute the "loudness" value
    loudness = librosa.feature.rms(S=librosa.db_to_amplitude(spec_dba)).mean()

    conn = get_db_connection()
    cur = conn.cursor()

    session["email"] = "maya"

    email = session["email"]
    cur.execute("SELECT teachers.teacherName FROM teachers, students, relationships where students.email = (?) AND students.email = relationships.studentEmail AND teachers.teacherEmail = relationships.teacherEmail", [email])
    teachers = cur.fetchall()
    conn.close()

    print(teachers)

    f = request.form
    print(f)

    return render_template("compare.html", zcrs=zcrs, cent=cent, mel=mel, loudness=loudness, teachers=teachers)

@app.route("/send_mail",methods=['POST','GET'])
def send_mail():
    msg = Message('Hello', sender = 'mayaNbridgman@gmail.com', recipients = ['m.athena138@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"

@app.route("/userprofile",methods=['POST','GET'])
def userprofile():
    conn = get_db_connection()
    cur = conn.cursor()
  
    if "email" in session:
        email = session["email"]

        cur.execute("SELECT email, firstName, lastName FROM students where email = (?)", [email])
        studentrow = cur.fetchone()
        conn.close()
        
        return redirect(url_for("userprofile"), email = studentrow[0], firstName = studentrow[1], lastName = studentrow[2])
    else:
        return "not logged in"

if __name__ =='__main__':
    app.run(host='localhost', port=5002, debug=True)

            #return(session["firstName"])
