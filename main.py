from flask import Flask
from flask import request
from flask import render_template
import os
import mysql.connector
from flask_mysqldb import MySQL
import mysql.connector
import re
app = Flask(__name__)

#configure db
connection = mysql.connector.connect(host='localhost', user='root', database='nea', password='')
#instantiate mysql module
mysql = MySQL(app)

@app.route("/login", methods=['POST', 'GET'])
def login():
    #if credentials are correct redirect to route home
    errormsg = 'incorrect info try again'
    #if login credentials have been posted
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

@app.route("/", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        #if login credentials have been posted
        email = request.form["email"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        password = request.form["password"]

        if email == "":
            return("Please enter an email")
        elif firstName == "":
            return("Please enter a first name")
        elif lastName == "":
            return("Please enter a last name")
        elif password == "":
            return("Please enter a password")

        if not re.search('^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{7,}$', password):
            return("Please enter a password that is over 7 characters, has upper and lower case letters, a number, and a special character")
        
        if not re.search('[a-z0-9]+@[a-z]+\.[a-z]{2,3}', email):
            return("Please enter a valid email address")
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (email, password))
        account = cur.fetchone()
        if account:
            return("Email already taken")
        else:
            cur.execute("INSERT INTO students(firstName, lastName, email, password) VALUES(%s, %s, %s, %s)", (firstName, lastName, email, password))
            mysql.connection.commit()
            cur.close()
            return("success")
    return render_template("signup.html")

if __name__ == "__main__":
    app.run()