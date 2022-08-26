DROP TABLE IF EXISTS relationships;

CREATE TABLE relationships (
    studentEmail TEXT NOT NULL,
    teacherEmail TEXT NOT NULL,
    PRIMARY KEY (studentEmail, teacherEmail)
);