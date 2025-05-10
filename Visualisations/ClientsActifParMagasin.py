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

query = """
SELECT s.store_id, COUNT(DISTINCT c.customer_id) AS nb_clients_actifs
FROM customer c
JOIN store s ON c.store_id = s.store_id
WHERE c.active = 1
GROUP BY s.store_id;
"""

df_clients = pd.read_sql(query, engine)

# Affichage graphique
plt.figure(figsize=(6,4))
sns.barplot(data=df_clients, x='store_id', y='nb_clients_actifs', palette='Set2', hue='store_id')
plt.title("Nombre de clients actifs par magasin")
plt.xlabel("ID du magasin")
plt.ylabel("Nombre de clients actifs")
print("Nombre de clients actifs par magasin")
plt.show()
