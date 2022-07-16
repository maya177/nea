from flask import Flask
from flask import request
from flask import render_template
import os
import mysql.connector

#connection = mysql.connector.connect(host='localhost', port='8889', database='', user='root', password='root')
#cursor = connection.cursor()
app = Flask(__name__)

@app.route("/login", methods=['POST', 'GET'])
def login():
    #if credentials are correct redirect to route home
    errormsg = 'incorrect info try again'
    #if login credentials have been posted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")
    #cursor.execute("select * from x where course=x")
    #value=cursor.fetchall()
    #return render_template("userprofile.html", data=value, name=x)

@app.route("/userprofile")
def userprofile():
    return("i am here")
    #cursor.execute("select * from x where course=x")
    #value=cursor.fetchall()
    #return render_template("userprofile.html", data=value, name=x)

#this is routing the url of the flask app
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        print(type(request.get_data("audio_data")))
        #f = open('./file.wav', 'wb')
        #f.write(request.get_data("audio_data"))
        #f.close()
        
        if os.path.isfile('./file.wav'):
            print("./file.wav exists")

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run()