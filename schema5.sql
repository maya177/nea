DROP TABLE IF EXISTS forgotPasswrd;

CREATE TABLE forgotPasswrd (
    email TEXT NOT NULL,
    recordTime INT NOT NULL,
    code INT NOT NULL,
    PRIMARY KEY(email, recordTime)
);