#connexion a Mysql avec SQLAlchemy
import os
import pandas as pd
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
#1. Total des locations
query = """
SELECT COUNT(*) AS total_locations
FROM rental;
"""
df_total_locations = pd.read_sql(query, engine)
print("Total des locations:", df_total_locations['total_locations'][0])

print()

#2. Client ayant loué le plus de films
query_client_max_locations = """
SELECT customer.first_name, customer.last_name, COUNT(r.rental_id) AS nb_locations
FROM customer
JOIN rental r ON customer.customer_id = r.customer_id
GROUP BY customer.customer_id
ORDER BY nb_locations DESC
LIMIT 1;
"""
df_client_max_locs = pd.read_sql(query_client_max_locations, engine)
print("Client ayant loué le plus de films:", df_client_max_locs['first_name'][0],
      df_client_max_locs['last_name'][0],
      "avec", df_client_max_locs['nb_locations'][0], "locations.")
print()

#3.répartition géographique des clients

query_repartition_ville =""" SELECT ci.city, COUNT(c.customer_id) AS nb_clients
FROM customer c
JOIN address a ON c.address_id = a.address_id
JOIN city ci ON a.city_id = ci.city_id
GROUP BY ci.city
ORDER BY nb_clients DESC;
"""

df_query_ville =pd.read_sql(query_repartition_ville, engine)
print("Répartition géographique des clients")
print(df_query_ville)
print()

#4.Clients inactifs

query_inactifClient = """SELECT DATE_FORMAT(rental_date, '%Y-%m') AS month, COUNT(DISTINCT customer_id) AS clients
FROM rental
GROUP BY month
ORDER BY month;"""

df_inactifClient =pd.read_sql(query_inactifClient,engine)
print("Clients inactifs")
print(df_inactifClient)

print()
#5.Clients actifs par magasin
query_client_magasin = """SELECT s.store_id, COUNT(DISTINCT c.customer_id) AS nb_clients_actifs
FROM customer c
JOIN store s ON c.store_id = s.store_id
WHERE c.active = 1
GROUP BY s.store_id;"""
df_client_magasin =pd.read_sql(query_client_magasin,engine)
print("Clients actifs par magasins")
print(df_client_magasin)