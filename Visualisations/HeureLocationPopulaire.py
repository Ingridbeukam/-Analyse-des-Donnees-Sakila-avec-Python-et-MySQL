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
# Heure de location populaire
query_heure = """
SELECT 
  HOUR(rental_date) AS heure,
  COUNT(*) AS nb_locations
FROM rental
GROUP BY heure
ORDER BY heure;
"""
df_heure = pd.read_sql(query_heure, engine)

plt.figure(figsize=(10,6))
sns.lineplot(data=df_heure, x='heure', y='nb_locations', marker='o', color="green")
plt.title("Nombre de locations par heure de la journée")
plt.xlabel("Heure (24h)")
plt.ylabel("Nombre de locations")
plt.xticks(range(0, 24))
plt.tight_layout()
print("Heure de location populaire")
print(df_heure)
plt.show()
