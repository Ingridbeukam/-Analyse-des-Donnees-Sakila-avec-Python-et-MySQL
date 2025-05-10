import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import seaborn as sns

# Charger les variables depuis .env
load_dotenv()

# Construire l'URL de connexion SQLAlchemy
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")

# Créer une engine SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")
print()
#Répartition des durées de films
query = "SELECT title, length FROM film WHERE length IS NOT NULL;"
df_length = pd.read_sql(query, engine)

# Visualisation
plt.figure(figsize=(10,6))
sns.histplot(df_length['length'], bins=20, kde=True, color="green")
plt.title("Répartition des durées de films")
plt.xlabel("Durée (minutes)")
plt.ylabel("Nombre de films")
plt.xlabel("Durée (minutes)")
print("Répartition des durées de films")
print(df_length)
plt.show()


print("""
L'analyse de la répartition des films par durée permet de comprendre combien de films 
dans la base Sakila durent un certain nombre de minutes.
Objectif:
Visualiser comment les films se répartissent selon leur durée. Par exemple :
Est-ce qu’il y a beaucoup de films courts (≤ 60 min) ?
Quelle est la durée la plus fréquente ?
Y a-t-il des films très longs (outliers) ?
""")