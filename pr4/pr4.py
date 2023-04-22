import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connectar amb la base de dades
conn = sqlite3.connect('pr4.db')

# Llegir les taules
defuncions_df = pd.read_sql_query("SELECT * from defuncions", conn)
densitat_df = pd.read_sql_query("SELECT * from densitat", conn)
ocupacio_df = pd.read_sql_query("SELECT * from ocupacio", conn)
conn.close()

# Mostrar les primeres cinc files de cada taula
# print("Defuncions:")
# print(defuncions_df.head())
# print("\nDensitat:")
# print(densitat_df.head())

# calcular la correlació entre les columnes "Densitat (hab/ha)" i "Nombre"
correlacio_defuncions = densitat_df["Densitat (hab/ha)"].corr(defuncions_df["Nombre"])
correlacio_ocupacio = densitat_df["Densitat (hab/ha)"].corr(ocupacio_df["Ocupacio_mitjana_(persones_ per_domicili)"])
print("La correlació entre densitat i nombre de defuncions és:", correlacio_defuncions)
print("La correlació entre densitat i ocupació mitjana és:", correlacio_ocupacio)

# Unir les taules
merged_defuncions_df = pd.merge(defuncions_df, densitat_df, on=['Codi_Districte', 'Codi_Barri'])
merged_ocupacion_df = pd.merge(ocupacio_df, densitat_df, on=['Codi_Districte', 'Codi_Barri'])

# Mostrar les primeres cinc files de la taula unida
# print("\nTaula unida:")
# print(merged_df.head())

# Crear el gràfic de dispersió
plt.scatter(merged_defuncions_df['Densitat (hab/ha)'], merged_defuncions_df['Nombre'])

# Afegir les etiquetes als eixos
plt.xlabel('Densitat de població (hab/ha)')
plt.ylabel('Nombre de defuncions')

# Mostrar el gràfic
plt.show()

# Crear el gràfic de dispersió
plt.scatter(merged_ocupacion_df['Densitat (hab/ha)'], merged_ocupacion_df['Ocupacio_mitjana_(persones_ per_domicili)'])

# Afegir les etiquetes als eixos
plt.xlabel('Densitat de població (hab/ha)')
plt.ylabel('Ocupació Mitjana')

# Mostrar el gràfic
plt.show()