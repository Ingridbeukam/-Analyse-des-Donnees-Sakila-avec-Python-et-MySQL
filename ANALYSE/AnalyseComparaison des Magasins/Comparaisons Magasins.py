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








