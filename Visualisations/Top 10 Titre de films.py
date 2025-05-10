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
print()

#	Analyse des films les plus populaires :
#Pour exemple, calculer les films les plus populaires (en termes de location) :

query = """
SELECT f.title, COUNT(*) AS total_rentals
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY total_rentals DESC
LIMIT 10;
"""
df = pd.read_sql(query, engine)
df.plot(kind='bar', x='title', y='total_rentals', title='Top 10 Titres de Films par Locations', color="brown")
print("les titres de films les plus populaires (en termes de location)")
print(df)
plt.show()
