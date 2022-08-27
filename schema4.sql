DROP TABLE IF EXISTS thresholds;

CREATE TABLE thresholds (
    studentEmail TEXT NOT NULL,
    recordTime INT NOT NULL,
    zcrs REAL NOT NULL,
    cent REAL NOT NULL,
    mel REAL NOT NULL,
    loudness REAL NOT NULL,
    totalThreshold REAL NOT NULL,
    PRIMARY KEY (studentEmail, recordTime)
);