DROP TABLE IF EXISTS students;

CREATE TABLE students (
    email TEXT PRIMARY KEY NOT NULL,
    firstName TEXT NOT NULL, 
    lastName TEXT NOT NULL,
    passwrd BINARY(16) NOT NULL
);