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
#2. Revenu total par magasin

query_revenu_magasin = """
SELECT store.store_id, SUM(payment.amount) AS revenu_total
FROM store
JOIN staff ON store.store_id = staff.store_id
JOIN payment ON staff.staff_id = payment.staff_id
GROUP BY store.store_id;
"""
df_revenu_magasin = pd.read_sql(query_revenu_magasin, engine)
print("Revenu total par magasin (CHF):")
print(df_revenu_magasin)
print()
# 3. Categorie le plus rentable
query_genre_rentable = """
SELECT c.name AS categorie, SUM(p.amount) AS revenu_total
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
JOIN film f ON fc.film_id = f.film_id
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY c.name
ORDER BY revenu_total DESC
LIMIT 1;
"""
Categorie_rentable = pd.read_sql(query_genre_rentable, engine)
print("La categorie du film la plus rentable est:",Categorie_rentable["categorie"][0])
print()
print(Categorie_rentable)

print()
# 4. Client ayant loué le plus de films
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

#5. Moyenne de durée de location (en jours)
query_avg_duration = """
SELECT AVG(DATEDIFF(r.return_date, r.rental_date)) AS avg_duration
FROM rental r;
"""
df_avg_duration = pd.read_sql(query_avg_duration, engine)
print("Moyenne de durée de location (en jours):", df_avg_duration['avg_duration'][0])
print()

# 6. Nombre moyen de locations par mois
query_avg_monthly_rentals = """
SELECT AVG(monthly_rentals) AS avg_monthly_rentals
FROM (
    SELECT COUNT(r.rental_id) AS monthly_rentals
    FROM rental r
    GROUP BY YEAR(r.rental_date), MONTH(r.rental_date)
) AS monthly_data;
"""
df_avg_monthly_rentals = pd.read_sql(query_avg_monthly_rentals, engine)
print("Nombre moyen de locations par mois:", df_avg_monthly_rentals['avg_monthly_rentals'][0])
print()

#7. Films les plus populaire en terme de location
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

# 8.Revenu total par catégorie de film

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

#9.répartition géographique des clients

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
#10.Nombre de locations par jour de la semaine

query_jour ="""SELECT 
  DAYNAME(rental_date) AS jour,
  COUNT(*) AS nb_locations
FROM rental
GROUP BY jour
ORDER BY FIELD(jour, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
"""
df_jour = pd.read_sql(query_jour,engine)
print("Nombre de locations par jour de la semaine")
print(df_jour)
print()
#11.Nombre de locations par heure

query_heure ="""SELECT 
  HOUR(rental_date) AS heure,
  COUNT(*) AS nb_locations
FROM rental
GROUP BY heure
ORDER BY heure;

"""
df_heure = pd.read_sql(query_heure,engine)
print("Nombre de locations par heure")
print(df_heure)


