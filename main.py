import json
from operator import truediv
from flask import Flask,request,render_template,session,url_for,redirect,jsonify
from flask_session import Session
from tempfile import mkdtemp
import hashlib
import sqlite3
import re

app = Flask(__name__)

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

@app.route('/',methods=['POST','GET'])
def signup():
    # if user is currently logged in
    if request.method=='POST':
        session.clear()
        conn = get_db_connection()

        email = request.form["email"]
        firstName = request.form["firstName"] 
        lastName = request.form["lastName"]
        passwrd = request.form["password"]

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
        
        return "add teachers here - success!"

    return render_template("signup.html")

@app.route('/addTeachers', methods=['POST','GET'])
def addTeachers():
    if request.method=='POST':
        print("getting data")
        im_dict = request.form
        #multi dictionary when multi field form?
        return(f'<h1>{im_dict}</h1>')

    return render_template("addTeachers.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        session.clear()

        conn = get_db_connection()
        cur = conn.cursor()

        email = request.form["email"]
        passwrd = hashlib.md5(request.form["password"].encode())

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


@app.route("/recorder")
def recorder():
    return render_template("recorder.html")


@app.route("/threshold", methods=['GET','POST'])
def threshold():
    if request.method == 'POST':
        try:
            #cannot use request.get_json()
            data = json.loads(request.data)
            return data
        except ValueError:
            return "Error" 
    else:
        return render_template("threshold.html")

@app.route("/userprofile",methods=['POST','GET'])
def userprofile():
    conn = get_db_connection()
    cur = conn.cursor()
  
    if "email" in session:
        email = session["email"]

        cur.execute("SELECT email, firstName, lastName FROM students where email = (?)", [email])
        studentrow = cur.fetchone()
        conn.close()
        print(studentrow[0])
        print(studentrow[1])
        print(studentrow[2])
        
        return render_template('userprofile.html', email = studentrow[0], firstName = studentrow[1], lastName = studentrow[2])
    else:
        return "not logged in"

if __name__ =='__main__':
    app.run(host='localhost', port=5002, debug=True)

            #return(session["firstName"])
