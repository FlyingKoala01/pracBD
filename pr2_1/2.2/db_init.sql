PRAGMA foreign_keys=ON;

CREATE TABLE usuari (
    email    VARCHAR(20)    PRIMARY KEY     NOT NULL,
    nom      TEXT                    NOT NULL,
    cognom   TEXT                    NOT NULL,
    poblacio TEXT                            ,
    pwd      TEXT                            
);

CREATE TABLE amistats (
    email1   TEXT                    NOT NULL,
    email2   TEXT                    NOT NULL,
    estat    TEXT                    NOT NULL,
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
INSERT INTO amistats values('isaac@isaac.net', 'abel@isaac.net', 'Acceptada');
INSERT INTO amistats values('isaac@isaac.net', 'abel@abel.net', 'Rebutjada');
INSERT INTO amistats values('ferran@isaac.net', 'eric@eric.net', 'Acceptada');

