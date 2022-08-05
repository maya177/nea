from flask import Flask
from flask import request
from flask import render_template
import os
import mysql.connector
from flask_mysqldb import MySQL
import mysql.connector
import re
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'main'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'NEA'

mysql = MySQL(app)
@app.route("/", methods=['POST', 'GET'])
def hello():
    return("Here")

if __name__ == "__main__":
    app.run()