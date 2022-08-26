import sqlite3

connection = sqlite3.connect('database.db')


with open('schema3.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

connection.commit()
connection.close()