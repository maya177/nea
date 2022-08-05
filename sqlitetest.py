import sqlite3

connection = sqlite3.connect("nea.db")
cursor = connection.cursor()

command = "create table if not exists students(studentID INT primary key, firstName TEXT, lastName TEXT, email TEXT, password TEXT"
cursor.execute(command)