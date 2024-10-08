-- Create database if not exists
CREATE DATABASE IF NOT EXISTS dinoco_anon;
USE dinoco_anon;

-- Ensure all tables use InnoDB
SET default_storage_engine=InnoDB;

-- table_a
CREATE TABLE table_a (
    col_a1 BIGINT PRIMARY KEY,
    col_a2 VARCHAR(255),
    col_a3 BIGINT,
    col_a4 BIGINT,
    col_a5 DATETIME
);

-- table_b
CREATE TABLE table_b (
    col_b1 VARCHAR(255),
    col_b2 BIGINT,
    col_b3 TEXT,
    col_b4 TEXT,
    col_b5 TEXT,
    PRIMARY KEY (col_b1, col_b2),
    FOREIGN KEY (col_b2) REFERENCES table_a(col_a1)
);

-- table_c
CREATE TABLE table_c (
    col_c1 BIGINT PRIMARY KEY,
    col_c2 TEXT,
    col_c3 TEXT,
    col_c4 TEXT,
    col_c5 TEXT,
    col_c6 TEXT,
    col_c7 BOOLEAN,
    col_c8 DATETIME,
    col_c9 DOUBLE,
    col_c10 DOUBLE
);

-- table_d
CREATE TABLE table_d (
    col_d1 BIGINT PRIMARY KEY,
    col_d2 BIGINT,
    col_d3 DATETIME,
    col_d4 DATETIME,
    col_d5 BIGINT,
    FOREIGN KEY (col_d1) REFERENCES table_a(col_a1)
);

-- table_e
CREATE TABLE table_e (
    col_e1 BIGINT,
    col_e2 BIGINT,
    col_e3 BIGINT,
    col_e4 DATETIME,
    col_e5 DATETIME,
    PRIMARY KEY (col_e1, col_e2),
    FOREIGN KEY (col_e2) REFERENCES table_d(col_d1)
);

-- table_f
CREATE TABLE table_f (
    col_f1 VARCHAR(255) PRIMARY KEY,
    col_f2 BIGINT
);

-- table_g
CREATE TABLE table_g (
    col_g1 BIGINT,
    col_g2 BIGINT,
    col_g3 VARCHAR(255),
    col_g4 BIGINT,
    col_g5 TEXT,
    col_g6 BIGINT,
    col_g7 TEXT,
    col_g8 DATETIME,
    col_g9 DATETIME,
    col_g10 VARCHAR(255),
    PRIMARY KEY (col_g1, col_g2),
    FOREIGN KEY (col_g1) REFERENCES table_d(col_d1),
    FOREIGN KEY (col_g10) REFERENCES table_f(col_f1)
);

-- table_h
CREATE TABLE table_h (
    col_h1 BIGINT,
    col_h2 BIGINT,
    col_h3 BIGINT,
    col_h4 BIGINT,
    col_h5 DATETIME,
    PRIMARY KEY (col_h1, col_h2, col_h3),
    FOREIGN KEY (col_h1, col_h2) REFERENCES table_e(col_e1, col_e2),
    FOREIGN KEY (col_h2, col_h3) REFERENCES table_g(col_g1, col_g2)
);

-- table_i
CREATE TABLE table_i (
    col_i1 BIGINT PRIMARY KEY,
    col_i2 BIGINT,
    col_i3 BIGINT,
    col_i4 BIGINT,
    col_i5 VARCHAR(255),
    col_i6 VARCHAR(255),
    col_i7 BIGINT,
    col_i8 VARCHAR(255),
    col_i9 BIGINT,
    col_i10 BIGINT,
    col_i11 VARCHAR(255),
    col_i12 DATETIME,
    col_i13 DATETIME,
    col_i14 TEXT,
    col_i15 TEXT,
    col_i16 VARCHAR(255),
    FOREIGN KEY (col_i2) REFERENCES table_d(col_d1),
    FOREIGN KEY (col_i3, col_i2) REFERENCES table_e(col_e1, col_e2),
    FOREIGN KEY (col_i16) REFERENCES table_f(col_f1)
);

-- table_j
CREATE TABLE table_j (
    col_j1 BIGINT,
    col_j2 BIGINT,
    col_j3 BIGINT,
    col_j4 BIGINT,
    col_j5 BIGINT,
    col_j6 TEXT,
    col_j7 TEXT,
    col_j8 DATETIME,
    col_j9 BIGINT,
    col_j10 BIGINT,
    col_j11 BIGINT,
    col_j12 DATETIME,
    PRIMARY KEY (col_j1, col_j2),
    FOREIGN KEY (col_j1) REFERENCES table_i(col_i1)
);