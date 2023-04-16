PRAGMA foreign_keys=ON;

-- Tables
CREATE TABLE IF NOT EXISTS departaments (
    numero INT PRIMARY KEY,
    nom VARCHAR(10) UNIQUE NOT NULL,
    localitzacio VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS empleats (
    codi INT PRIMARY KEY,
    cognom VARCHAR(10),
    ofici VARCHAR(10),
    data_alta DATE,
    salari INT,
    comissio_preventes INT,
    departament INT NOT NULL,
    cap INT,

    FOREIGN KEY (departament) REFERENCES departaments(numero),
    FOREIGN KEY (cap) REFERENCES empleats(codi)

);

CREATE TABLE IF NOT EXISTS clients (
    codi INT PRIMARY KEY,
    nom VARCHAR(10),
    adreca VARCHAR(10),
    CP INT,
    telefon INT,
    limit_credit INT,
    observacions_destacades VARCHAR(10),
    empleat INT NOT NULL,

    FOREIGN KEY (empleat) REFERENCES empleats(codi)
);

CREATE TABLE IF NOT EXISTS productes (
    codi INT PRIMARY KEY,
    descripcio VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS comandes (
    codi INT PRIMARY KEY,
    data_time DATE,
    tipus VARCHAR(10),
    codi_client VARCHAR(10),
    data_tramesa DATE,
    import_total INT,

    FOREIGN KEY (codi_client)  REFERENCES clients(codi)
);

CREATE TABLE IF NOT EXISTS detall (
    codiComanda INT NOT NULL,
    codiProducte INT NOT NULL,
    quantitat INT,
    preu INT,

    PRIMARY KEY (codiComanda, codiProducte),
    FOREIGN KEY (codiComanda)  REFERENCES comandes(codi),
    FOREIGN KEY (codiProducte) REFERENCES productes(codi)
);

INSERT INTO departaments (numero, nom, localitzacio) VALUES
    (10, 'Vendes', 'Barcelona'),
    (20, 'Marketing', 'Madrid'),
    (30, 'Desenvolupament', 'València');

INSERT INTO empleats (codi, cognom, ofici, data_alta, salari, comissio_preventes, departament, cap) VALUES
    (7369, 'Smith', 'Empleat', '1980-12-17', 800, NULL, 20, 7902),
    (7499, 'Allen', 'Venedor', '1981-02-20', 1600, 300, 30, 7698),
    (7521, 'Ward', 'Venedor', '1981-02-22', 1250, 500, 30, 7698),
    (7566, 'Jones', 'Director', '1981-04-02', 2975, NULL, 20, 7839),
    (7654, 'Martin', 'Venedor', '1981-09-28', 1250, 1400, 30, 7698),
    (7698, 'Blake', 'Director', '1981-05-01', 2850, NULL, 30, 7839),
    (7782, 'Clark', 'Director', '1981-06-09', 2450, NULL, 10, 7839),
    (7788, 'Scott', 'Analista', '1982-12-09', 3000, NULL, 20, 7566),
    (7839, 'Rey', 'President', '1981-11-17', 5000, NULL, 10, NULL),
    (7844, 'Turner', 'Venedor', '1981-09-08', 1500, 0, 30, 7698),
    (7876, 'Adams', 'Empleat', '1983-01-12', 1100, NULL, 20, 7788),
    (7900, 'James', 'Empleat', '1981-12-03', 950, NULL, 30, 7698),
    (7902, 'Ford', 'Analista', '1981-12-03', 3000, NULL, 20, 7566),
    (7934, 'Miller', 'Empleat', '1982-01-23', 1300, NULL, 10, 7782);

INSERT INTO clients (codi, nom, adreca, CP, telefon, limit_credit, observacions_destacades, empleat) VALUES
    (1, 'ACME', 'Carrer Major, 1', 08001, 934123456, 10000, 'Pagament a 30 dies', 7369),
    (2, 'Google', 'Avinguda Diagonal, 100', 08019, 932123456, 50000, NULL, 7521),
    (3, 'Apple', 'Passeig de Gràcia, 100', 08008, 931123456, 80000, 'Bon client', 7698),
    (4, 'Microsoft', 'Gran Via, 400', 08015, 935123456, 25000, NULL, 7521),
    (5, 'Amazon', 'Rambla de Catalunya, 200', 08008, 936123456, 75000, 'Pagament a 60 dies', 7698);

INSERT INTO productes (codi, descripcio) VALUES
    (1, 'Ordinador portàtil'),
    (2, 'Monitor'),
    (3, 'Ratolí'),
    (4, 'Teclat'),
    (5, 'Impressora');

INSERT INTO comandes (codi, data_time, tipus, codi_client, data_tramesa, import_total) VALUES
    (1, '2023-04-16 10:00:00', 'Online', 1, '2023-04-18', 2000),
    (2, '2023-04-16 12:00:00', 'Presencial', 2, '2023-04-17', 10000),
    (3, '2023-04-16 14:00:00', 'Online', 3, '2023-04-19', 5000),
    (4, '2023-04-16 16:00:00', 'Presencial', 4, '2023-04-20', 2500),
    (5, '2023-04-16 18:00:00', 'Online', 5, '2023-04-21', 7500); 

INSERT INTO detall (codiComanda, codiProducte, quantitat, preu) VALUES
    (1, 1, 2, 1000),
    (1, 2, 1, 500),
    (2, 3, 5, 50),
    (2, 4, 3, 100),
    (2, 5, 2, 200),
    (3, 1, 1, 1000),
    (3, 4, 1, 100),
    (3, 5, 3, 200),
    (4, 2, 2, 750),
    (4, 3, 1, 50),
    (5, 1, 3, 900),
    (5, 3, 2, 50),
    (5, 5, 1, 500);

-- 1) 
-- SELECT e.codi, e.cognom, d.numero, d.nom 
-- FROM empleats e 
-- INNER JOIN departaments d ON e.departament = d.numero;

-- 2)
-- SELECT d.numero, d.nom, MAX(e.salari) AS "MaxSalary"
-- FROM departaments d 
-- INNER JOIN empleats e ON e.departament = d.numero 
-- GROUP BY d.numero, d.nom;

-- 4)
-- SELECT c.*, e.cognom AS "Representative"
-- FROM clients c 
-- INNER JOIN empleats e ON c.empleat = e.codi;

-- 7)
-- SELECT e.*
-- FROM empleats e 
-- INNER JOIN (
--  SELECT departament, AVG(salari) AS "AvgSalary" 
--  FROM empleats 
--  GROUP BY departament
-- ) AS avgs ON e.departament = avgs.departament 
-- WHERE e.salari > avgs.AvgSalary;

-- 8)
-- SELECT * FROM empleats WHERE ofici = (SELECT ofici FROM empleats WHERE cognom = 'SALA');

-- 9)
-- SELECT nom, ofici FROM empleats WHERE departament = 20 AND ofici IN (SELECT ofici FROM empleats WHERE departament = (SELECT numero FROM departaments WHERE nom = 'VENDES'));

-- 10)
-- SELECT * FROM empleats WHERE ofici = 'NEGRO' OR salari >= (SELECT salari FROM empleats WHERE cognom = 'GIL');

-- 11)
-- SELECT empleats.codi, empleats.cognom, departaments.nom FROM empleats JOIN departaments ON empleats.departament = departaments.numero WHERE empleats.codi IN (SELECT cap FROM empleats) ORDER BY empleats.cognom;

-- 12)
-- SELECT departament, SUM(salari) AS import_global FROM empleats GROUP BY departament ORDER BY import_global DESC;

-- 13)
-- SELECT departament, MIN(data_alta) AS antiguitat FROM empleats GROUP BY departament ORDER BY antiguitat ASC;

-- 14)
-- SELECT empleats.codi, empleats.cognom, COUNT(comandes.codi) AS nombre_comandes FROM empleats LEFT JOIN clients ON empleats.codi = clients.empleat LEFT JOIN comandes ON clients.codi = comandes.codi_client GROUP BY empleats.codi, empleats.cognom ORDER BY empleats.cognom;

-- 15)
-- SELECT empleats.codi, empleats.cognom, COUNT(comandes.codi) AS nombre_comandes FROM empleats LEFT JOIN clients ON empleats.codi = clients.empleat LEFT JOIN comandes ON clients.codi = comandes.codi_client GROUP BY empleats.codi, empleats.cognom HAVING COUNT(comandes.codi) > 3 ORDER BY COUNT(comandes.codi) DESC;

-- 16)
-- SELECT productes.codi, productes.descripcio, detall.preu, comandes.data_time FROM productes JOIN detall ON productes.codi = detall.codiProducte JOIN comandes ON detall.codiComanda = comandes.codi WHERE comandes.data_time = (SELECT MAX(data_time) FROM comandes);

-- 17)
-- SELECT clients.codi, clients.nom FROM clients JOIN comandes ON clients.codi = comandes.codi_client WHERE YEAR(comandes.data_time) = 2016 AND comandes.import_total > (clients.limit_credit * 0.5);