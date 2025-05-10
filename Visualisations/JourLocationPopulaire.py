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

# Les jours de location les plus populaires

query_jour = """
SELECT 
  DAYNAME(rental_date) AS jour,
  COUNT(*) AS nb_locations
FROM rental
GROUP BY jour
ORDER BY FIELD(jour, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday');
"""
df_jour = pd.read_sql(query_jour, engine)

plt.figure(figsize=(10,6))
sns.barplot(data=df_jour, x='jour', y='nb_locations', palette='coolwarm', hue='jour')
plt.title("Nombre de locations par jour de la semaine")
plt.xlabel("Jour")
plt.ylabel("Nombre de locations")
print("Les jours de location les plus populaires")
print(df_jour)
plt.show()
