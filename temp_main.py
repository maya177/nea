import json
from flask import Flask,request,render_template,session,url_for,redirect,jsonify
from flask_session import Session
from tempfile import mkdtemp
import hashlib
import sqlite3
import re
import librosa
import json
import numpy as np
from datetime import datetime
import smtplib
from flask import *
from random import randint


now = datetime.now()
app = Flask(__name__)

#setting up SMTP email server
sender_email = "mayaNbridgman@gmail.com"
receiver_email = ""
password = "lboesehsgspqsxny"
SUBJECT = ""
TEXT = ""
msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
server = smtplib.SMTP("smtp.gmail.com", 587)
 
#sessions used to store user information in a temporary directory on flask server instead of using cookies
app.config["SESSION_FILE_DIR" ]= mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#start the Flask session
app.config.from_object(__name__)
Session(app)

#connecting to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

##user redirects instead of render template as it re requests form i think

@app.route('/',methods=['POST','GET'])
def signup():

    #there is a POST request if user is currently logged in
    if request.method=='POST':
        session.clear()
        conn = get_db_connection()

        #retrieving user input
        email = request.form.get("email", False)
        firstName = request.form.get("firstName", False)
        lastName = request.form.get("lastName", False)
        passwrd = request.form.get("password", False)

        #validating empty fields
        if not email:
            flash("Please enter an email")
            return redirect("/")
        elif not firstName:
            flash("Please enter a first name")
            return redirect("/")
        elif not lastName:
            flash("Please enter a last name")
            return redirect("/")
        elif not passwrd:
            flash("Please enter a password")
            return redirect("/")
        
        #validating password to ensure complexity
        if not re.search("^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{7,}$", passwrd):
            flash("Please enter a password that is over 7 characters, has upper and lower case letters, a number, and a special character")
            return redirect("/")

        passwrd =  hashlib.md5(passwrd.encode())

        #validating email input
        if not re.search("[a-z0-9]+@[a-z]+\.[a-z]{2,3}", email):
            flash("Please enter a valid email address")
            return redirect("/")
        try:
            #inserting data into database
            conn.execute("INSERT INTO students (firstName,lastName,email,passwrd) VALUES(?,?,?,?)",(firstName,lastName,email,passwrd.hexdigest()))
            conn.commit()
            conn.close()

        except sqlite3.IntegrityError:
            flash("Email already in the system, enter another email")
            return redirect("/")

        #set user session
        session["email"] = email
        session["firstName"] = firstName
        session["lastName"] = lastName
        
        return redirect(url_for("addTeachers"))

    return render_template("signup.html")

@app.route('/addTeachers', methods=['POST','GET'])
def addTeachers():
    if request.method=='POST':
        print("receiving data")

        conn = get_db_connection()
        im_dict = request.form
        #data is retrieved as a multi-dictionary so cannot be selected by im_dict[i]
        items = list(im_dict.items())

        for i in range(len(items)):           
            if i%2 == 0:
                teacherName = items[i][1]
                teacherEmail = items[i+1][1]

                conn.execute("INSERT INTO teachers (teacherEmail,teacherName) VALUES(?,?)",(teacherEmail,teacherName))
                conn.commit()

                try:
                    studentEmail = session["email"]
                    conn.execute("INSERT INTO relationships (studentEmail,teacherEmail) VALUES(?,?)",(studentEmail,teacherEmail))
                    conn.commit()
                except:
                    flash("please log in")
                    return redirect(url_for("login"))
        conn.close()
                
        return redirect(url_for("home"))

    return render_template("addTeachers.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        session.clear()

        conn = get_db_connection()
        cur = conn.cursor()

        #retrieve email and password inputted by user
        email = request.form.get("email", False)
        passwrd = hashlib.md5(request.form.get("password").encode())

        #validating empty fields
        if not email:
            flash("please enter an email")
            return redirect("/login")
        elif not passwrd:
            flash("please enter a passwrd")
            return redirect("/login")

        #retrieving user information from database
        cur.execute("SELECT email, passwrd, firstName, lastName FROM students where email = (?)", [email])
        studentrow = cur.fetchone()
        conn.close()

        try:
            #checking if password inputted matches password from database
            if passwrd.hexdigest() == studentrow[1]:
                session["email"] = email
                session["firstName"] = studentrow[2]
                session["lastName"] = studentrow[3]
                return render_template("home.html")
            else:
                flash("incorrect password")
                return redirect("/login")
        except:
           flash("this account does not exist, please sign up")
           return redirect("/")

    return render_template("login.html")
            
@app.route('/forgotPasswrd', methods=['POST','GET'])
def forgotPasswrd():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()

        #retrieves student email from database
        email = request.form.get("email", False)
        cur.execute("SELECT email FROM students where email = (?)", [email])
        studentEmail = cur.fetchone()
        
        if len(studentEmail) == 0:
            flash("This email does not exist, enter another email")
            return redirect("/forgotPasswrd")
        else:
            session["resetEmail"] = email
            session["resetPasswrd"] = True
            print(session["resetPasswrd"])

            #creating code and inserting it into database
            code = randint(1000000,9999999)
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            conn.execute("INSERT INTO forgotPasswrd (email,recordTime,code) VALUES(?,?,?)",(email,date_time,code))
            conn.commit()
            conn.close()

            #sending email over SMTP server to user
            server.starttls()
            server.login(sender_email, password)
            receiver_email = email
            SUBJECT = "Password reset code"
            TEXT = f"Your password reset code is {code}"

            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            server.sendmail(sender_email, receiver_email, msg)
            server.quit()

            return redirect(url_for("forgotPasswrdCode"))

    return render_template("forgotPasswrd.html")


@app.route('/forgotPasswrdCode', methods=['POST','GET'])
def forgotPasswrdCode():
    if "resetPasswrd" in session:
        if session["resetPasswrd"] == True:
            if request.method == 'POST':

                email = session["resetEmail"]
                conn = get_db_connection()
                cur = conn.cursor()

                #select most recent password reset code from database
                getCode = request.form.get("code", False)
                cur.execute("SELECT code FROM forgotPasswrd where email = (?) ORDER BY recordTime DESC", [email])
                code = cur.fetchone()
                conn.close()

                if len(code) != 1:
                    return("wrong code")
                else:
                    if str(getCode) == str(code[0]):
                        return redirect("/resetPasswrd")
                    else:
                        return("wrong code")
        else:
            flash("Please reset password from here")
            return redirect(url_for("forgotPasswrd"))
    else:
        flash("Please reset password from here")
        return redirect(url_for("forgotPasswrd"))
        
    return render_template("forgotPasswrdCode.html")


@app.route('/resetPasswrd', methods=['POST','GET'])
def resetPasswrd():
        if session["resetPasswrd"] == True:
            if request.method == 'POST':
   
                email = session["resetEmail"]
                conn = get_db_connection()
                cur = conn.cursor()

                passwrd = request.form.get("passwrd", False)

                #validating inputted password
                if not re.search("^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{7,}$", passwrd):
                    flash("Please enter a password that is over 7 characters, has upper and lower case letters, a number, and a special character")
                    return redirect("/resetPasswrd")
                
                newPasswrd = hashlib.md5(passwrd.encode())

                #updating database record to new password 
                cur.execute("UPDATE students set passwrd = (?) WHERE email = (?)", (str(newPasswrd.hexdigest()), str(email)))
                conn.commit()

                conn.close()
                return redirect(url_for("login"))

        else: 
            flash("Please reset password from here")
            return redirect(url_for("login"))
 
        return render_template("resetPasswrd.html")


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
        #retrieves audio data and stores file locally
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M")
        f = open(f'./static/recordings/{filename}.wav', 'wb')
        f.write(request.data)
        f.close()

        #the 'x' variable stores the audio data and the 'fs' variable stores the sampling rate in Hertz of the audio recorded
        x, fs = librosa.load(f'./static/recordings/{filename}.wav')

        session["x"] = x
        session["fs"] = fs

        response = jsonify("File received and saved!")
        return response
    
    return render_template("recorder.html")

##literally spent 1.5 hrs figuring out that ajax doesn't do normal redirects, had to implement success function in js that one tutorial lied

@app.route("/threshold1", methods=['GET','POST'])
def threshold1():    
    if request.method == 'POST':
        try:
            #using JavaScript success function to redirect to threshold2 page
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except:
            flash("error, try again")
            return redirect("/threshold1")
    return render_template("threshold1.html")
   
@app.route("/threshold2", methods=['GET','POST'])
def threshold2():
    if request.method == 'POST':
        try:
            data = request.get_json()
            volume = data['volume']
            freq = data['pitch']
            path = data['src']
            #x is audio points, fs is sample rate
            #t_ indicates temporary use
            t_x, t_fs = librosa.load(path)

            #zero crossing rate mean value extracted
            zcrs = librosa.feature.zero_crossing_rate(t_x).mean()
            #central spectroid mean value extracted
            cent = librosa.feature.spectral_centroid(y=t_x, sr=t_fs).mean()
            #converting the sample rate to the mel scale to represent frequency
            mel = 2595.0 * np.log10(1.0 + t_fs / 700.0)

            ##loudness - Root Mean Square - value extracted
            #computing the magnitude spectrogram
            n_fft = 2048
            hop_length = 1024
            spec_mag = abs(librosa.stft(t_x, n_fft=n_fft, hop_length=hop_length))
            #converting the spectogram into decibels
            spec_db = librosa.amplitude_to_db(spec_mag)
            #calculating A-weighting values
            freqs = librosa.fft_frequencies(sr=t_fs, n_fft=n_fft)
            a_weights = librosa.A_weighting(freqs)
            a_weights = np.expand_dims(a_weights, axis=1)
            #applying A-weighting values to magnitude spectogram
            spec_dba = spec_db + a_weights
            #calculating final loudness value
            loudness = librosa.feature.rms(S=librosa.db_to_amplitude(spec_dba)).mean()

            zcrs = zcrs*freq
            cent = cent*freq
            mel = mel*freq
            loudness = loudness*volume

            totalThreshold = zcrs/2 + mel/2 + cent/2 + 5*(1-loudness.exp(10*-1))
            if "email" in session:
                totalThreshold = 1
                conn = get_db_connection()
                studentEmail = session["email"]
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

                conn.execute("INSERT INTO thresholds (studentEmail,recordTime,zcrs,cent,mel,loudness,totalThreshold) VALUES(?,?,?,?,?,?,?)", (studentEmail,date_time,zcrs,cent,mel,loudness,totalThreshold))
                conn.commit()
                conn.close()

                return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        except ValueError:
            flash("error")
            return redirect("/threshold2")
    else:
        return render_template("threshold2.html")

@app.route('/compare', methods = ['GET','POST'])
def compare():
    #set up connections/sessions
    conn = get_db_connection()
    cur = conn.cursor()

    if 'x' in session:
        x = session["x"]
        fs = session["fs"]
        email = session["email"]

        #----------------------------------------------------------------------
        ##extract audio features of recorded audio
        #zero crossing rate
        zcrs = librosa.feature.zero_crossing_rate(x).mean()
        #central spectroid
        cent = librosa.feature.spectral_centroid(y=x, sr=fs).mean()
        #mel scale converted freq
        mel = 2595.0 * np.log10(1.0 + fs / 700.0)

        #loudness in rms
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
        #----------------------------------------------------------------------
        #calculate final values of recorded audio

        zcrs = round(zcrs,2)
        cent = round(cent,2)
        mel = round(mel,2)
        loudness = round(loudness,2)

        audioTotalThreshold = zcrs/2 + mel/2 + cent/2 + 5*(1-loudness.exp(10*-1))

        #----------------------------------------------------------------------
        try:
            cur.execute("SELECT zcrs, cent, mel, loudness, totalThreshold FROM thresholds where studentEmail = (?) ORDER BY recordTime DESC", [email])
            rec_threshold = cur.fetchone()

            t_zcrs = rec_threshold[0]
            t_cent = rec_threshold[1]
            t_mel = rec_threshold[2]
            t_loudness = rec_threshold[3]
            t_total= rec_threshold[4]
        except:
            return redirect(url_for("threshold"))

        #----------------------------------------------------------------------
        #compare total thresholds

        if audioTotalThreshold < t_total:
            comp = "The current audio level is below your recorded threshold"
        else:
            comp = "The current audio level is above your recorded threshold"

        #----------------------------------------------------------------------
        #get teachers/send to teachers
        cur.execute("""SELECT teachers.teacherName FROM teachers, students, relationships where students.email = (?) 
        AND students.email = relationships.studentEmail AND teachers.teacherEmail = relationships.teacherEmail""", [email])
        teachers = cur.fetchall()

        if request.method == 'POST':
            server.starttls()
            server.login(sender_email, password)

            teacherName = request.form["teacher"]

            cur.execute("SELECT teacherEmail FROM teachers where teacherName = (?)", [teacherName])
            teacherEmail = cur.fetchone()


            cur.execute("SELECT firstName FROM students where email = (?)", [email])
            studentName = cur.fetchone()

            receiver_email = teacherEmail
            SUBJECT = "Attend to child"
            if audioTotalThreshold > t_total:
                exceed = "exceeded"
            else:
                exceed = "did not exceed"
            TEXT = f"{studentName[0]}'s threshold of {t_total} {exceed} the classroom noise level of {audioTotalThreshold}, please check on them"
            msg = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            server.sendmail(sender_email, receiver_email, msg)
            server.quit()
            return redirect(url_for("home"))

        conn.close()
        return render_template("compare.html", zcrs=zcrs, cent=cent, mel=mel, loudness=loudness, teachers=teachers, comp=comp)

    else:
        flash("no audio recorded")
        return redirect(url_for("recorder"))
        

@app.route("/userprofile",methods=['POST','GET'])
def userprofile():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if "email" in session:
        #retrieving user data from database
        email = session["email"]

        cur.execute("SELECT email, firstName, lastName FROM students where email = (?)", [email])
        studentrow = cur.fetchone()
        conn.close()
        
        return render_template(("userprofile.html"), email = studentrow[0], firstName = studentrow[1], lastName = studentrow[2])
    else:
        flash("not logged in, please log in")
        return redirect(url_for("login"))



@app.route("/editTeachers",methods=['POST','GET'])
def editTeachers():
    conn = get_db_connection()
    cur = conn.cursor()
    
    if "email" in session:
        email = session["email"]

        cur.execute("SELECT teachers.teacherName, teachers.teacherEmail FROM teachers,students,relationships where students.email = (?) and relationships.studentEmail = students.email and relationships.teacherEmail = teachers.teacherEmail", [email])
        teachers = cur.fetchall()
        conn.close()
        
        return render_template("editTeachers.html", teachers=teachers)
    else:
        flash("not logged in, please log in")
        return redirect(url_for("login"))

@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        email = session['email']

        #retrieve teacher to change from user input on web page
        teacherName = request.form['teacherName']
        teacherEmail = request.form['teacherEmail']

        #allow user to input new teacher information
        if teacherName == '':
            msg = 'Please enter a teacher name'
        elif teacherEmail == '':
            msg = 'Please enter a teacher email'
        else:
            cur.execute("SELECT teacherName, teacherEmail FROM teachers where teacherEmail = (?)", [teacherEmail])
            teacherRow = cur.fetchall()
            
            cur.execute("SELECT teacherEmail, studentEmail FROM relationships where studentEmail =? and teacherEmail=?", (str(email), teacherEmail))
            relationshipRow = cur.fetchall()

            #if relationship between teacher and student already exists then do not add new relationship
            if len(relationshipRow) != 0:
                return jsonify("This teacher is already linked to this account")
            #if teacher already exists in 'teachers' but not in relationship with student, add relationship with student
            elif len(teacherRow) != 0:
                print("working")
                conn.execute("INSERT INTO relationships (studentEmail,teacherEmail) VALUES (?,?)", (str(email),teacherEmail))
                conn.commit()
            
            #if teacher does not exist in 'teachers', add to 'teachers' and 'relationships'
            #this is because a teacher must exist in 'teachers' to be in 'relationships'
            else:
                print(teacherEmail, teacherName)
                conn.execute("INSERT INTO teachers (teacherEmail,teacherName) VALUES (?,?)", (teacherEmail, teacherName))
                conn.commit()

                conn.execute("INSERT INTO relationships (studentEmail,teacherEmail) VALUES (?,?)", (str(email),teacherEmail))
                conn.commit()

            conn.close()
            msg = 'new record created successfully'
        
    return jsonify(msg)

@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        #retrieve user input from web page
        getEmail = request.form['string']
        teacherName = request.form['teacherName']
        teacherEmail = request.form['teacherEmail']

        #update teacher information in database
        conn.execute("UPDATE teachers SET teacherEmail = ?, teacherName = ? WHERE teacherEmail = ? ", (teacherEmail, teacherName, getEmail))
        conn.execute("UPDATE relationships SET teacherEmail = ? WHERE teacherEmail = ? ", (teacherEmail, getEmail))

        conn.commit()
        cur.close()
        msg = 'Record successfully Updated'
    return jsonify(msg)

@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete(): 
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        getEmail = request.form['string']

        #delete record from 'teachers' and 'relationships'
        conn.execute('DELETE FROM teachers WHERE teacherEmail = ?', [getEmail])
        conn.execute('DELETE FROM relationships WHERE teacherEmail = ?', [getEmail])

        conn.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg) 

if __name__ =='__main__':
    app.run(host='localhost', port=5002, debug=True)