PRAGMA foreign_keys=ON;

CREATE TABLE usuari (
    email    TEXT PRIMARY KEY,
    nom      TEXT NOT NULL,
    cognom   TEXT NOT NULL,
    poblacio TEXT NOT NULL,
    pwd      TEXT NOT NULL                         
);

CREATE TABLE amistats (
    email1   TEXT NOT NULL,
    email2   TEXT NOT NULL,
    estat    TEXT NOT NULL,
    PRIMARY KEY (email1, email2),
    FOREIGN KEY (email1) REFERENCES usuari,
    FOREIGN KEY (email2) REFERENCES usuari
);

-- Filling the db
INSERT INTO usuari values('isaac@isaac.net', 'Isaac', 'Iglesias', 'Navarcles', '1234isaac');
INSERT INTO usuari values('eric@eric.net', 'Eric', 'Roy', 'Manresa', '1234eric');
INSERT INTO usuari values('gabri@gabri.net', 'Gabri', 'Quino', 'Barxato', '1234bruc');
INSERT INTO usuari values('josep@josep.net', 'Josep', 'Suca', 'Avinyo','1234josep');
INSERT INTO usuari values('abel@abel.net', 'Abel', 'Lai', 'Navarcles','1234abel');
INSERT INTO usuari values('ferran@ferran.net', 'Ferran', 'Casa', 'Navarcles','1234ferran');

INSERT INTO amistats values('isaac@isaac.net', 'eric@eric.net', 'Acceptada');
INSERT INTO amistats values('isaac@isaac.net', 'gabri@gabri.net', 'Acceptada');
INSERT INTO amistats values('isaac@isaac.net', 'josep@josep.net', 'Rebutjada');
INSERT INTO amistats values('isaac@isaac.net', 'abel@abel.net', 'Rebutjada');
INSERT INTO amistats values('ferran@ferran.net', 'eric@eric.net', 'Acceptada');

-- Exercici1
SELECT email, nom, cognom, poblacio FROM usuari WHERE poblacio = 'Manresa';
-- Exercici2
SELECT email FROM usuari WHERE cognom = 'Casa';
-- Exercici3 ( Amics de Ferran Casa )
SELECT email, nom, cognom, poblacio
FROM usuari
WHERE email IN (
  SELECT email1
  FROM amistats
  WHERE email2 IN (SELECT email FROM usuari WHERE nom = 'Ferran' AND cognom = 'Casa') AND estat = 'Acceptada'
)
OR email IN (
  SELECT email2
  FROM amistats
  WHERE email1 IN (SELECT email FROM usuari WHERE nom = 'Ferran' AND cognom = 'Casa') AND estat = 'Acceptada'
);
-- Exercici 4 ( Amics de Ferran Casa que no siguin amics de Gabri )
SELECT email, nom, cognom, poblacio
FROM usuari
WHERE email IN (
  SELECT email1
  FROM amistats
  WHERE email2 IN (SELECT email FROM usuari WHERE nom = 'Ferran' AND cognom = 'Casa') AND estat = 'Acceptada'
)
OR email IN (
  SELECT email2
  FROM amistats
  WHERE email1 IN (SELECT email FROM usuari WHERE nom = 'Ferran' AND cognom = 'Casa') AND estat = 'Acceptada'
)
EXCEPT
SELECT email, nom, cognom, poblacio
FROM usuari
WHERE email IN (
  SELECT email1
  FROM amistats
  WHERE email2 IN (SELECT email FROM usuari WHERE nom = 'Gabri') AND estat = 'Acceptada'
)
OR email IN (
  SELECT email2
  FROM amistats
  WHERE email1 IN (SELECT email FROM usuari WHERE nom = 'Gabri') AND estat = 'Acceptada'
);
-- Exercici 5
SELECT COUNT(*) AS total_rebutjades
FROM amistats
WHERE estat = 'Rebutjada';
-- Exercici 6
SELECT nom, cognom
FROM usuari
WHERE email IN (
    SELECT email1
    FROM amistats
    WHERE email2 IN (
        SELECT email
        FROM usuari
        WHERE poblacio = 'Manresa'
    ) AND estat = 'Acceptada'
) OR email IN (
    SELECT email2
    FROM amistats
    WHERE email1 IN (
        SELECT email
        FROM usuari
        WHERE poblacio = 'Manresa'
    ) AND estat = 'Acceptada'
);
-- Exercici 7
SELECT email, nom, cognom,
       (SELECT COUNT(*) FROM amistats WHERE email1 = usuari.email AND estat = 'Rebutjada') AS num_peticions_rebutjades
FROM usuari;
-- Exercici 8
SELECT *
FROM usuari
WHERE email NOT IN (
    SELECT email1 FROM amistats WHERE email2 = (
        SELECT email FROM usuari WHERE cognom = 'Casa' AND nom = 'Ferran'
    ) AND estat = 'Acceptada'
) AND email NOT IN (
    SELECT email2 FROM amistats WHERE email1 = (
        SELECT email FROM usuari WHERE cognom = 'Casa' AND nom = 'Ferran'
    ) AND estat = 'Acceptada'
);
