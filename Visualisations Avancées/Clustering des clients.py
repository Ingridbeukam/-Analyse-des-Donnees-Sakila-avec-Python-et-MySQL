#connexion a Mysql
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

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



# Extrait des données clients (ex : total paiement et nombre de locations)
query = """
SELECT c.customer_id, COUNT(r.rental_id) AS nb_locations, SUM(p.amount) AS total_revenu
FROM customer c
JOIN rental r ON c.customer_id = r.customer_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.customer_id;
"""
df_clients = pd.read_sql(query, engine)

# Prétraitement
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clients[["nb_locations", "total_revenu"]])

# Clustering K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
df_clients["cluster"] = kmeans.fit_predict(X_scaled)

# Visualisation
plt.figure(figsize=(8, 5))
plt.scatter(df_clients["nb_locations"], df_clients["total_revenu"], c=df_clients["cluster"], cmap="viridis")
plt.xlabel("Nombre de locations")
plt.ylabel("Total payé")
plt.title("Segmentation des clients")
print("Segmentation des clients")
print(df_clients)
plt.show()

print()
print("""Objectif : Segmenter les clients en groupes homogènes pour mieux comprendre 
leur comportement d'achat.
Méthode : Utilisation de l'algorithme K-Means sur les données de locations 
et de revenu pour identifier 3 groupes de clients.
Résultats : Visualisation des clusters et analyse des segments de clients, 
permettant de cibler des actions marketing spécifiques selon les besoins 
des groupes identifiés (par exemple, fidélisation des clients à fort potentiel).

Conclusion
Le clustering K-Means vous permet de diviser les clients en groupes ayant des 
comportements similaires. Cette segmentation est utile pour 
personnaliser l'expérience client, créer des stratégies de fidélisation adaptées 
et optimiser les offres de services.

""")