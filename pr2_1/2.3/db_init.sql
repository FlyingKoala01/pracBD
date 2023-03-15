PRAGMA foreign_keys=ON;

CREATE TABLE empleat (
    id_empleat INT PRIMARY KEY,
    carrer TEXT,
    ciutat TEXT NOT NULL
    );

CREATE TABLE feina (
    id_empleat INT PRIMARY KEY,
    id_empresa INT NOT NULL,
    salari FLOAT NOT NULL,
    FOREIGN KEY (id_empleat) REFERENCES empleat,
    FOREIGN KEY (id_empresa) REFERENCES empresa
    );

CREATE TABLE empresa (
    id_empresa INT PRIMARY KEY,
    ciutat TEXT NOT NULL
    );

CREATE TABLE manager (
    id_empleat INT PRIMARY KEY,
    id_empleat_coordinador INT NOT NULL,
    FOREIGN KEY (id_empleat) REFERENCES empleat,
    FOREIGN KEY (id_empleat_coordinador) REFERENCES empleat
    );

-- Filling the db
INSERT INTO empleat (id_empleat, carrer, ciutat) VALUES
(1, 'Carrer de la Lluna', 'Barcelona'),
(2, 'Carrer de la Sol', 'Barcelona'),
(3, 'Carrer del Riu', 'Madrid'),
(4, 'Carrer del Bosc', 'Madrid'),
(5, 'Carrer del Mar', 'València'),
(6, 'Carrer del Cel', 'València');

INSERT INTO empresa (id_empresa, ciutat) VALUES
(1, 'Barcelona'),
(2, 'Madrid'),
(3, 'València');

INSERT INTO feina (id_empleat, id_empresa, salari) VALUES
(1, 1, 2000.00),
(2, 1, 2200.00),
(3, 2, 1800.00),
(4, 2, 1900.00),
(5, 3, 1700.00),
(6, 3, 1850.00);

INSERT INTO manager (id_empleat, id_empleat_coordinador) VALUES
(1, 2),
(3, 4),
(5, 6);

-- Exercici 1 (empresa no té camp de nom, pel que suposarem que bank newton es id 2)
SELECT id_empleat, ciutat
FROM empleat
WHERE id_empleat IN (
    SELECT id_empleat
    FROM feina
    WHERE id_empresa = 2
);
-- Exercici 2
SELECT *
FROM empleat
WHERE id_empleat IN (
    SELECT id_empleat
    FROM feina
    WHERE id_empresa = 2 AND salari > 2000
);
-- Exercici 3
SELECT id_empleat
FROM empleat
WHERE id_empleat NOT IN (
    SELECT id_empleat
    FROM feina
    WHERE id_empresa = 2
);
-- Exercici 4
SELECT *
FROM empleat
WHERE id_empleat IN (
    SELECT id_empleat
    FROM feina
    WHERE salari > (
        SELECT MAX(salari)
        FROM feina
        WHERE id_empresa = 2
    )
);
-- Exercici 5
SELECT id_empresa, COUNT(id_empleat) AS total_empleats
FROM feina
GROUP BY id_empresa
ORDER BY total_empleats DESC
LIMIT 1;
-- Exercici 6
UPDATE empleat
SET ciutat = 'Manresa'
WHERE id_empleat = 2;
-- Exercici 7
UPDATE feina
SET salari = salari * 1.1
WHERE id_empleat IN (
    SELECT id_empleat_coordinador
    FROM manager
);
-- Exercici 8
SELECT id_empleat
FROM empleat
WHERE ciutat = (
    SELECT ciutat
    FROM empresa
    WHERE id_empresa = (
        SELECT id_empresa
        FROM (
            SELECT id_empleat, id_empresa
            FROM feina
        ) AS feina_empleat
        WHERE feina_empleat.id_empleat = empleat.id_empleat
    )
);
-- Exercici 9
SELECT id_empleat
FROM empleat
WHERE ciutat = (
    SELECT ciutat
    FROM empleat
    WHERE id_empleat IN (
        SELECT id_empleat_coordinador
        FROM manager
        WHERE id_empleat = empleat.id_empleat
    )
    LIMIT 1);
-- Exercici 10
DELETE FROM feina
WHERE id_empresa = 2;

