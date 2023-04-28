-- PRACTICA 4 PART 2 : Triggers
-- Eric Roy & Isaac Iglesias

drop table if exists usuaris;
drop table if exists amistats;
drop table if exists preferencies;

create table usuaris(ID int, nom text, grau int);
create table amistats(ID1 int, ID2 int);
create table preferencies(ID1 int, ID2 int);


insert into usuaris values (1510, 'Jordan', 9);
insert into usuaris values (1689, 'Gabriel', 9);
insert into usuaris values (1381, 'Tiffany', 9);
insert into usuaris values (1709, 'Cassandra', 9);
insert into usuaris values (1101, 'Haley', 10);
insert into usuaris values (1782, 'Andrew', 10);
insert into usuaris values (1468, 'Kris', 10);
insert into usuaris values (1641, 'Brittany', 10);
insert into usuaris values (1247, 'Alexis', 11);
insert into usuaris values (1316, 'Austin', 11);
insert into usuaris values (1911, 'Gabriel', 11);
insert into usuaris values (1501, 'Jessica', 11);
insert into usuaris values (1304, 'Jordan', 12);
insert into usuaris values (1025, 'John', 12);
insert into usuaris values (1934, 'Kyle', 12);
insert into usuaris values (1661, 'Logan', 12);

insert into amistats values (1510, 1381);
insert into amistats values (1510, 1689);
insert into amistats values (1689, 1709);
insert into amistats values (1381, 1247);
insert into amistats values (1709, 1247);
insert into amistats values (1689, 1782);
insert into amistats values (1782, 1468);
insert into amistats values (1782, 1316);
insert into amistats values (1782, 1304);
insert into amistats values (1468, 1101);
insert into amistats values (1468, 1641);
insert into amistats values (1101, 1641);
insert into amistats values (1247, 1911);
insert into amistats values (1247, 1501);
insert into amistats values (1911, 1501);
insert into amistats values (1501, 1934);
insert into amistats values (1316, 1934);
insert into amistats values (1934, 1304);
insert into amistats values (1304, 1661);
insert into amistats values (1661, 1025);
insert into amistats select ID2, ID1 from amistats; 

insert into preferencies values(1689, 1709);
insert into preferencies values(1709, 1689);
insert into preferencies values(1782, 1709);
insert into preferencies values(1911, 1247);
insert into preferencies values(1247, 1468);
insert into preferencies values(1641, 1468);
insert into preferencies values(1316, 1304);
insert into preferencies values(1501, 1934);
insert into preferencies values(1934, 1501);
insert into preferencies values(1025, 1101);

-- TASCA 1
----------
DROP TABLE IF EXISTS amicsPotencials;
CREATE TABLE amicsPotencials(ID1 INT, ID2 INT);

CREATE TRIGGER afegirPotencials AFTER INSERT ON usuaris
WHEN new.grau IS NOT NULL
BEGIN
    INSERT INTO amicsPotencials (ID1, ID2)
        SELECT new.ID, usuaris.ID
        FROM usuaris
        WHERE usuaris.grau = new.grau AND usuaris.ID != new.ID;
END;

-- Exemple d'us:
-- sqlite> insert into usuaris values (3, 'jonny', 9);
-- sqlite> select * from amicsPotencials;
-- 3|1510
-- 3|1689
-- 3|1381
-- 3|1709

-- TASCA 2
----------
CREATE TRIGGER grauPerDefecte AFTER INSERT ON usuaris
WHEN new.grau IS NULL
BEGIN
    UPDATE usuaris SET grau = 9 WHERE usuaris.ID = new.ID;
END;

CREATE TRIGGER validarGrau AFTER INSERT ON usuaris
WHEN new.grau > 12 OR new.grau < 9
BEGIN
    UPDATE usuaris SET grau = NULL WHERE usuaris.ID = new.ID;
END;

-- Exemple d'us:
-- sqlite> insert into usuaris values (4, 'michael', 982345), (5, 'francesco', NULL);
-- sqlite> .header on
-- sqlite> .mode column
-- sqlite> select * from usuaris where ID in (4,5);
-- ID          nom         grau      
-- ----------  ----------  ----------
-- 4           michael               
-- 5           francesco   9   

-- TASCA 3
----------

CREATE TRIGGER eliminarAmistat AFTER DELETE ON amistats
BEGIN
    DELETE FROM amistats WHERE old.ID1 = amistats.ID2 AND old.ID2 = amistats.ID1;
END;

CREATE TRIGGER afegirAmistat AFTER INSERT ON amistats
BEGIN
    INSERT INTO amistats VALUES (new.ID2, new.ID1);
END;

-- Exemple d'us:
-- sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
-- sqlite> insert into amistats values (4,5);
-- sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
-- 4|5
-- 5|4
-- sqlite> delete from amistats where ID1 = 4 and ID2 = 5;
-- sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
-- sqlite> 

-- TASCA 4
----------

CREATE TRIGGER eliminarGraduat AFTER UPDATE OF grau ON usuaris
WHEN new.grau > 12
BEGIN
    DELETE FROM usuaris WHERE usuaris.ID = old.ID;
END;

-- Extra, eliminar elements referenciats en cascada:
CREATE TRIGGER eliminarReferenciesUsuari AFTER DELETE ON usuaris
BEGIN
    DELETE FROM preferencies WHERE ID1 = old.ID OR ID2 = old.ID;
    DELETE FROM amistats WHERE ID1 = old.ID;
    -- El trigger d'amistats anterior ja eliminarà el cas ID2 = old.ID;
END;

-- Exemple d'us:
-- sqlite> select * from usuaris where ID = 1510;
-- 1510|Jordan|9
-- sqlite> update usuaris set grau=24 where ID = 1510;
-- sqlite> select * from usuaris where ID = 1510;
-- sqlite> select * from amistats where ID1 = 1510 OR ID2 = 1510;
-- sqlite> select * from preferencies where ID1 = 1510 OR ID2 = 1510;
-- sqlite> 


-- TASCA 5
CREATE TRIGGER incrementarGrau AFTER UPDATE OF grau ON usuaris
WHEN new.grau = old.grau+1
BEGIN
    UPDATE usuaris SET grau = grau + 1
    WHERE usuaris.ID IN (
        SELECT ID2 FROM amistats WHERE ID1 = old.ID
        );
END;


-- Exemple d'us:
-- sqlite> select * from usuaris inner join amistats on usuaris.ID = amistats.ID1 where amistats.ID2 = 1689;
-- ID          nom         grau        ID1         ID2       
-- ----------  ----------  ----------  ----------  ----------
-- 1709        Cassandra   9           1709        1689      
-- 1782        Andrew      10          1782        1689      
-- sqlite> update usuaris set grau=grau+1 where ID = 1689;
-- sqlite> select * from usuaris inner join amistats on usuaris.ID = amistats.ID1 where amistats.ID2 = 1689;
-- ID          nom         grau        ID1         ID2       
-- ----------  ----------  ----------  ----------  ----------
-- 1709        Cassandra   10          1709        1689      
-- 1782        Andrew      11          1782        1689      
-- sqlite> 

-- TASCA 6
CREATE TRIGGER eliminarCanviPreferencia AFTER UPDATE of ID2 ON preferencies
BEGIN
    DELETE FROM amistats WHERE amistats.ID1 = old.ID2 AND amistats.ID2 = new.ID2;
    -- Només eliminem una direcció de l'amistat ja que hi ha un trigger que fa la resta.
END;

-- Exemple d'us:
-- sqlite> select * from amistats where ID1 = 1689 and ID2 = 1782;
-- ID1         ID2       
-- ----------  ----------
-- 1689        1782      
-- sqlite> select * from preferencies where ID1 = 1709 and ID2 = 1689;
-- ID1         ID2       
-- ----------  ----------
-- 1709        1689      
-- sqlite> update preferencies set ID2 = 1782 where ID1 = 1709;
-- sqlite> select * from amistats where ID1 = 1689 and ID2 = 1782;
-- sqlite> 
