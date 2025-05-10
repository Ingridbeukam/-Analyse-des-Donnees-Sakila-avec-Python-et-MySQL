#connexion a Mysql
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

#2. Films les plus populaire en terme de location
query_populaire = """SELECT f.title, COUNT(*) AS total_rentals
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY total_rentals DESC
LIMIT 10;"""
df_film_populaire = pd.read_sql(query_populaire,engine)
print("Films les plus populaire en terme de location")
print(df_film_populaire)
print()

#3.Revenu total par catégorie de film

query_revenu_categorie = """SELECT c.name AS category, SUM(p.amount) AS revenue
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film_category fc ON i.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY revenue DESC;"""
df_revenue = pd.read_sql(query_revenu_categorie, engine)
print("Revenu total par catégorie de film")
print(df_revenue)
print()




