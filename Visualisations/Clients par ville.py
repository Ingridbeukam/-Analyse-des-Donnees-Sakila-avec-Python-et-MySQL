#connexion a Mysql
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

print("connexion reussie")
print()

#Répartition géographique des clients
query = """
SELECT ci.city, COUNT(c.customer_id) AS nb_clients
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
GROUP BY ci.city
ORDER BY nb_clients DESC;
"""
df_ville = pd.read_sql(query, engine)

# Visualisation
plt.figure(figsize=(12,6))
sns.barplot(data=df_ville.head(15), x='nb_clients', y='city', palette='crest', hue='nb_clients')
plt.title("Top 15 villes par nombre de clients")
plt.xlabel("Nombre de clients")
plt.ylabel("Ville")
print("répartition géographique des clients")
print(df_ville)
plt.show()
