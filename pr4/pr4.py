import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

QUERIES = [
    "SELECT Codi_Barri, Nom_Barri, AVG(Pes_atur) AS 'atur_percent' FROM atur GROUP BY Codi_Barri ORDER BY Codi_Barri;",
    "SELECT d.Codi_Barri, d.Nom_Barri, SUM(d.Nombre)*1000.0/o.Població AS 'defuncions_permil' \
        FROM defuncions d INNER JOIN densitat o ON d.Codi_Barri = o.Codi_Barri GROUP BY d.Codi_Barri ORDER BY d.Codi_Barri;",
    "SELECT Codi_Barri, Nom_Barri, densitat.'Densitat neta (hab/ha)' AS 'densitat' FROM densitat ORDER BY Codi_Barri;"
]

# Connectar amb la base de dades
conn = sqlite3.connect('pr4.db')

# Llegir les taules
defuncions_df = pd.read_sql_query(QUERIES[1], conn)
atur_df = pd.read_sql_query(QUERIES[0], conn)
densitat_df = pd.read_sql_query(QUERIES[2], conn)
conn.close()

# calcular la correlació
densitat_df["densitat"] = pd.to_numeric(densitat_df["densitat"])

correlacio_atur = densitat_df["densitat"].corr(atur_df["atur_percent"])
print("La correlació entre densitat i atur és:", correlacio_atur)

correlacio_mortalitat = densitat_df["densitat"].corr(defuncions_df["defuncions_permil"])
print("La correlació entre densitat i mortalitat és:", correlacio_mortalitat)

# Unir les taules
merged_atur = pd.merge(densitat_df, atur_df, on=['Codi_Barri'])
merged_mortalitat = pd.merge(densitat_df, defuncions_df, on=['Codi_Barri'])

# Create a figure with two subplots side by side
fig, axs = plt.subplots(ncols=2, figsize=(12, 5))

# subplot - Atur
axs[0].scatter(merged_atur['densitat'], merged_atur['atur_percent'])
axs[0].set_xlabel('Densitat (hab/ha)')
axs[0].set_ylabel('Atur (%)')
axs[0].set_title(f'Atur: r = {correlacio_atur:.4f}')

# subplot - Mortalitat
axs[1].scatter(merged_mortalitat['densitat'], merged_mortalitat['defuncions_permil'])
axs[1].set_xlabel('Densitat (hab/ha)')
axs[1].set_ylabel('Mortalitat (‰)')
axs[1].set_title(f'Mortalitat: r = {correlacio_mortalitat:.4f}')

fig.suptitle('Correlació', fontsize=16, fontweight='bold')
plt.show()
