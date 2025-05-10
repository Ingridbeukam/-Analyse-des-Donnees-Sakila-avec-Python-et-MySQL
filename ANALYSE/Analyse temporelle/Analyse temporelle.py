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


#1. Moyenne de durée de location (en jours)
query_avg_duration = """
SELECT AVG(DATEDIFF(r.return_date, r.rental_date)) AS avg_duration
FROM rental r;
"""
df_avg_duration = pd.read_sql(query_avg_duration, engine)
print("Moyenne de durée de location (en jours):", df_avg_duration['avg_duration'][0])
print()

#2. Nombre moyen de locations par mois
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

#3.Nombre de locations par jour de la semaine

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
#4.Nombre de locations par heure

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


