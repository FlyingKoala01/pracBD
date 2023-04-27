# Pràctica 4 Bases de Dades

Isaac Iglesias & Eric Roy

## Obtenció dels fitxers CSV (any 2019)

En aquesta entrega s'adjunta, per comoditat, els fixters ja descarregats.
Tanmateix, es podrien descarregar:

Defuncions segons barri: https://opendata-ajuntament.barcelona.cat/data/dataset/2f90d889-cfc3-4775-a895-93558b844002/resource/5550de77-7119-495f-a591-1ba0afa571f6/download/2019_defuncions_lloc-de-naixement.csv

Ocupació segons barri: https://opendata-ajuntament.barcelona.cat/data/dataset/56568d9d-651a-49ff-bbc8-52d3fcee4421/resource/35619477-6bb3-4211-b4a2-3b85013f1d66/download/2019_padro_ocupacio_mitjana.csv

Atur segons barri: https://opendata-ajuntament.barcelona.cat/data/dataset/10dd343a-e81a-4f1f-9f95-e21b1ee71dcc/resource/0f1ed6a5-1224-4dec-94ee-92b542ad3c20/download

## Inicialització de la base de dades

En aquesta entrega s'adjunta, per comoditat, la base de dades ja creada.
Tanmateix, es podria crear de nou:

```
$ sqlite3 pr4.db
sqlite> .mode csv
sqlite> .import csv/2019_defuncions.csv defuncions
sqlite> .import csv/2019_ocupacio.csv ocupacio
sqlite> .import csv/2019_atur.csv atur
sqlite> .import csv/2019_densitat.csv densitat
sqlite> .tables
atur        defuncions  densitat    ocupacio
```
## Visualització dels gràfics

Executar el fitxer de python3 adjuntat en aquesta entrega.

## Conclusions

Com es pot observar amb la regresió calculada, aquesta està molt lluny de 1 o -1,
per tant, es pot concloure que no hi ha relació directe entre la densitat i la
mortalitat o atur.
