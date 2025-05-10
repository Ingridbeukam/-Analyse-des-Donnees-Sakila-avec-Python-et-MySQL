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
#Revenu total par catégorie de film
query = """
SELECT c.name AS category, SUM(p.amount) AS revenue
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film_category fc ON i.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY revenue DESC;
"""

df_revenue = pd.read_sql(query, engine)

# Visualisation
plt.figure(figsize=(10,6))
sns.barplot(data=df_revenue, x='revenue', y='category', palette='viridis', hue="category")
plt.title("Revenu total par catégorie de film")
plt.xlabel("Revenu")
plt.ylabel("Catégorie")
print("Revenu total par catégorie de film")
print(df_revenue)
plt.show()
