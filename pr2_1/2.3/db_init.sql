PRAGMA foreign_keys=ON;

CREATE TABLE empleat (
    id-empleat NUMERIC PRIMARY KEY,
    carrer   TEXT NOT NULL,
    ciutat   VARCHAR(20)
    );

CREATE TABLE feina (
    id-empleat NUMERIC PRIMARY KEY,
    id-empresa NUMERIC,
    salari NUMERIC,
    FOREIGN KEY (id-empleat) REFERENCES empleat,
    FOREIGN KEY (id-empresa) REFERENCES empresa
    );

CREATE TABLE empresa (
    id-empresa NUMERIC PRIMARY KEY,
    ciutat VARCHAR(20)
    );

CREATE TABLE manager (
    id-empleat NUMERIC PRIMARY KEY,
    id-empleat-empresa NUMERIC,
    FOREIGN KEY (id-empleat) REFERENCES empleat
    );

-- Filling the db

INSERT INTO empleat values (1, 'x1', 'BCN');
INSERT INTO empleat values (2, 'x2', 'BCN');
INSERT INTO empleat values (3, 'x2', 'BCN');
INSERT INTO empleat values (4, 'x3', 'MANRESA');
INSERT INTO empleat values (5, 'x3', 'TERRASA');
INSERT INTO empleat values (6, 'x2', 'SURIA');
INSERT INTO empleat values (7, 'x4', 'LLEIDA');
INSERT INTO empleat values (8, 'x5', 'MANRESA');
INSERT INTO empleat values (9, 'x8', 'BCN');

INSERT INTO feina values (1, 1, 'BCN');
INSERT INTO feina values (2, 1, 'BCN');
INSERT INTO feina values (3, 1, 'BCN');
INSERT INTO feina values (4, 35, 'MANRESA');
INSERT INTO feina values (5, 1, 'TERRASA');
INSERT INTO feina values (6, 35, 'SURIA');
INSERT INTO feina values (7, 21, 'LLEIDA');
INSERT INTO feina values (8, 1, 'MANRESA');
INSERT INTO feina values (9, 35, 'BCN');

INSERT INTO empresa values (1, 'BCN');
INSERT INTO empresa values (35, 'MANRESA');
INSERT INTO empresa values (21, 'LLEIDA');



