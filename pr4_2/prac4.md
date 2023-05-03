# PRÀCTICA 4 : Triggers

Fet per Isaac Iglesias i Eric Roy. Assignatura de Bases de Dades (EMIT),
curs 2022/2023.

*Per a reduir l'extensió del document, no es copien els enunciats sencers.*

## TASCA 1

Gestió de la taula `amicsPotencials`:

```sql
DROP TABLE IF EXISTS amicsPotencials;
CREATE TABLE amicsPotencials(ID1 INT, ID2 INT);

CREATE TRIGGER afegirPotencials AFTER INSERT ON usuaris
WHEN new.grau IS NOT NULL
FOR EACH ROW
BEGIN
    INSERT INTO amicsPotencials (ID1, ID2)
        SELECT new.ID, usuaris.ID
        FROM usuaris
        WHERE usuaris.grau = new.grau AND usuaris.ID != new.ID;
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```
sqlite> insert into usuaris values (3, 'jonny', 9);
sqlite> select * from amicsPotencials;
3|1510
3|1689
3|1381
3|1709
```

## TASCA 2

Gestió del grau dels usuaris:

```sql
CREATE TRIGGER grauPerDefecte AFTER INSERT ON usuaris
WHEN new.grau IS NULL
FOR EACH ROW
BEGIN
    UPDATE usuaris SET grau = 9 WHERE usuaris.ID = new.ID;
END;

CREATE TRIGGER validarGrau AFTER INSERT ON usuaris
WHEN new.grau > 12 OR new.grau < 9
FOR EACH ROW
BEGIN
    UPDATE usuaris SET grau = NULL WHERE usuaris.ID = new.ID;
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```
sqlite> insert into usuaris values (4, 'michael', 982345), (5, 'francesco', NULL);
sqlite> select * from usuaris where ID in (4,5);
ID          nom         grau      
----------  ----------  ----------
4           michael               
5           francesco   9  
``` 

## TASCA 3

Gestió de la bidireccionalitat de les amistats:

```sql
CREATE TRIGGER eliminarAmistat AFTER DELETE ON amistats
FOR EACH ROW
BEGIN
    DELETE FROM amistats WHERE old.ID1 = amistats.ID2 AND old.ID2 = amistats.ID1;
END;

CREATE TRIGGER afegirAmistat AFTER INSERT ON amistats
FOR EACH ROW
BEGIN
    INSERT INTO amistats VALUES (new.ID2, new.ID1);
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```sql
sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
sqlite> insert into amistats values (4,5);
sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
4|5
5|4
sqlite> delete from amistats where ID1 = 4 and ID2 = 5;
sqlite> select * from amistats where ID1 = 4 OR ID2 = 4;
sqlite>
```

## TASCA 4

Eliminar estudiants graduats:

```sql
CREATE TRIGGER eliminarGraduat AFTER UPDATE OF grau ON usuaris
WHEN new.grau > 12
FOR EACH ROW
BEGIN
    DELETE FROM usuaris WHERE usuaris.ID = old.ID;
END;
```

Per a evitar elements referenciats a objectes eliminats, hem
d'esborrar les preferències i amistats que referenciin al graduat:

```sql
CREATE TRIGGER eliminarReferenciesUsuari AFTER DELETE ON usuaris
FOR EACH ROW
BEGIN
    DELETE FROM preferencies WHERE ID1 = old.ID OR ID2 = old.ID;
    DELETE FROM amistats WHERE ID1 = old.ID;
    -- El trigger d'amistats de la tasca 3 ja eliminarà
    -- els casos ID2 = old.ID;
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```sql
sqlite> select * from usuaris where ID = 1510;
1510|Jordan|9
sqlite> update usuaris set grau=24 where ID = 1510;
sqlite> select * from usuaris where ID = 1510;
sqlite> select * from amistats where ID1 = 1510 OR ID2 = 1510;
sqlite> select * from preferencies where ID1 = 1510 OR ID2 = 1510;
```

## TASCA 5

Increment del grau dels amics/amigues:

```sql
-- Important que no sigui recursiu!
CREATE TRIGGER incrementarGrau AFTER UPDATE OF grau ON usuaris
WHEN new.grau = old.grau+1
FOR EACH ROW
BEGIN
    UPDATE usuaris SET grau = grau + 1
    WHERE usuaris.ID IN (
        SELECT ID2 FROM amistats WHERE ID1 = old.ID
        );
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```
sqlite> select * from usuaris inner join amistats on usuaris.ID = amistats.ID1 where amistats.ID2 = 1689;
ID          nom         grau        ID1         ID2       
----------  ----------  ----------  ----------  ----------
1709        Cassandra   9           1709        1689      
1782        Andrew      10          1782        1689      
sqlite> update usuaris set grau=grau+1 where ID = 1689;
sqlite> select * from usuaris inner join amistats on usuaris.ID = amistats.ID1 where amistats.ID2 = 1689;
ID          nom         grau        ID1         ID2       
----------  ----------  ----------  ----------  ----------
1709        Cassandra   10          1709        1689      
1782        Andrew      11          1782        1689      
```

## TASCA 6

Eliminar amistat quan es canvia la preferència:

```sql
CREATE TRIGGER eliminarCanviPreferencia AFTER UPDATE of ID2 ON preferencies
FOR EACH ROW
BEGIN
    DELETE FROM amistats WHERE amistats.ID1 = old.ID2 AND amistats.ID2 = new.ID2;
    -- Només eliminem una direcció de l'amistat ja que hi ha un trigger que fa la resta.
END;
```

Exemples d'ús (partint de la base de dades de l'enunciat):

```
sqlite> select * from amistats where ID1 = 1689 and ID2 = 1782;
ID1         ID2       
----------  ----------
1689        1782      
sqlite> select * from preferencies where ID1 = 1709 and ID2 = 1689;
ID1         ID2       
----------  ----------
1709        1689      
sqlite> update preferencies set ID2 = 1782 where ID1 = 1709;
sqlite> select * from amistats where ID1 = 1689 and ID2 = 1782;
```
