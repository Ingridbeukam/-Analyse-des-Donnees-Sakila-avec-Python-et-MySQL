import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Charger les variables depuis .env
load_dotenv()

# Construire l'URL de connexion SQLAlchemy
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")

# Créer une engine SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

print("connexion reussie")
print()

#1. Afficher Toutes les tables
query = "SHOW TABLES;"
df_table = pd.read_sql(query, engine)
print("Liste de toute les tables de la base de données Sakila")
print(df_table)

print()

#2.Examiner les structures des tables
query_structure = "DESCRIBE film;"
df_structure = pd.read_sql(query_structure, engine)
print("Structure de la table film:",df_structure)


#3 Examiner toutes les tables
tables = pd.read_sql("SHOW TABLES;", engine)
table_names = tables.iloc[:, 0].tolist()  # Extraire les noms des tables

# Étape 2 : Décrire chaque table
for table in table_names:
    print(f"🔍 Structure de la table : {table}")
    df_desc = pd.read_sql(f"DESCRIBE {table};", engine)
    print(df_desc)
    print("\n" + "-"*60 + "\n")

