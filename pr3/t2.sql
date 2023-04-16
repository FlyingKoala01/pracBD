-- Prac3

PRAGMA foreign_keys=ON;

-- Tables
CREATE TABLE IF NOT EXISTS clients (
    nif VARCHAR(10) PRIMARY KEY,
    raoSocial VARCHAR(10),
    addr VARCHAR(10),
    telefon INT,
    descompte INT
);

CREATE TABLE IF NOT EXISTS centres (
    codi INT PRIMARY KEY,
    ciutat VARCHAR(10),
    zona VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS venedors (
    codi INT PRIMARY KEY,
    nom VARCHAR(10),
    edat INT,
    codiCentre INT NOT NULL,

    FOREIGN KEY (codiCentre) REFERENCES centres(codi)
);

CREATE TABLE IF NOT EXISTS productes (
    codi INT PRIMARY KEY,
    descripcio VARCHAR(10),
    preu INT NOT NULL,
    estoc INT
);

CREATE TABLE IF NOT EXISTS comandes (
    numComanda INT PRIMARY KEY,
    codiProducte INT NOT NULL,
    codiVenedor INT NOT NULL,
    nif VARCHAR(10) NOT NULL,
    datatime INT,
    unitats INT,

    FOREIGN KEY (codiProducte) REFERENCES productes(codi),
    FOREIGN KEY (codiVenedor)  REFERENCES venedors(codi),
    FOREIGN KEY (nif)          REFERENCES clients(nif)
);

-- Clients:
INSERT INTO clients (nif, raoSocial, addr, telefon, descompte) VALUES
('12345678A', 'Client 1', 'Carrer Gran Via 1', 932222222, 10),
('87654321B', 'Client 2', 'Carrer Passeig 2', 934444444, 5),
('11111111A', 'Client 3', 'Carrer Balmes 12', 935555555, 0),
('22222222B', 'Client 4', 'Carrer Mallorca 24', 936666666, 15),
('33333333C', 'Client 5', 'Carrer Provença 36', 937777777, 5),
('44444444D', 'Client 6', 'Carrer Gran de Gracia 48', 938888888, 20),
('55555555E', 'Client 7', 'Carrer Arago 60', 939999999, 0);

-- Centres:
INSERT INTO centres (codi, ciutat, zona) VALUES
(1, 'Barcelona', 'Centre'),
(2, 'Madrid', 'Nord'),
(3, 'Barcelona', 'Nord'),
(4, 'Valencia', 'Est');

-- Venedors:
INSERT INTO venedors (codi, nom, edat, codiCentre) VALUES
(1, 'Venedor 1', 30, 1),
(2, 'Venedor 2', 24, 2),
(3, 'Venedor 3', 40, 3),
(4, 'Venedor 4', 35, 4),
(5, 'Venedor 5', 28, 1),
(6, 'Venedor 6', 26, 1),
(7, 'Venedor 7', 32, 3);

-- Productes:
INSERT INTO productes (codi, descripcio, preu, estoc) VALUES
(1, 'Producte 1', 10, 100),
(2, 'Producte 2', 20, 50),
(3, 'Producte 3', 15, 200),
(4, 'Producte 4', 25, 150),
(5, 'Producte 5', 30, 100),
(6, 'Producte 6', 40, 75),
(7, 'Producte 7', 20, 300),
(8, 'Producte 8', 5, 0),
(9, 'Producte 9', 30, 0);

-- Comandes:
INSERT INTO comandes (numComanda, codiProducte, codiVenedor, nif, datatime, unitats) VALUES
(1, 1, 1, '12345678A', '2023-04-16 10:23:00', 2),
(2, 2, 2, '87654321B', '2023-04-15 14:50:00', 3),
(3, 3, 3, '11111111A', '2023-04-14 09:15:00', 1),
(4, 4, 4, '22222222B', '2023-04-13 17:30:00', 2),
(5, 5, 5, '33333333C', '2023-04-12 11:45:00', 4),
(6, 1, 6, '44444444D', '2023-04-11 13:20:00', 1),
(7, 2, 7, '55555555E', '2023-04-10 16:50:00', 3);

-- DELETE FROM productes WHERE estoc = 0;

-- UPDATE clients SET descompte = 1.5 WHERE nif IN (SELECT nif FROM clients ORDER BY ROWID LIMIT 3);
 
--

-- SELECT centres.ciutat, centres.zona, venedors.nom, venedors.edat FROM centres INNER JOIN venedors ON venedors.codiCentre=centres.codi WHERE edat > 20 AND edat < 27 ORDER BY edat;

-- SELECT c.nif, SUM(p.preu * co.unitats * (1 - c.descompte/100)) AS total_import
--  FROM clients c
--  JOIN comandes co ON c.nif = co.nif
--  JOIN productes p ON co.codiProducte = p.codi
--  WHERE SUBSTR(co.datatime, 1, 4) = '2023'
--  GROUP BY c.nif;

-- SELECT v.nom, SUM(c.unitats) as total_units_sold
--  FROM venedors v
--  INNER JOIN comandes c ON v.codi = c.codiVenedor
--  GROUP BY v.codi
--  ORDER BY total_units_sold DESC
--  LIMIT 10;

-- SELECT p.*
--   FROM productes p
--  LEFT JOIN comandes c ON p.codi = c.codiProducte
--  WHERE c.numComanda IS NULL;