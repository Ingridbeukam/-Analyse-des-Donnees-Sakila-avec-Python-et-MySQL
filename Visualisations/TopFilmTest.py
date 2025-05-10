#connexion a Mysql
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Charger les variables depuis .env
load_dotenv()

# Connexion à MySQL
connexion = mysql.connector.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

print("Connexion réussie :", connexion.is_connected())

query = "SELECT * FROM customer;"
df = pd.read_sql(query, connexion)
print(df.head())

#1.Top des Categories de films
df = pd.read_sql("""
SELECT c.name AS category, COUNT(*) AS total_rentals
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY total_rentals DESC
""", connexion)

df.plot(kind="bar", x="category", y="total_rentals", title="Top genres de films")
print(df)
plt.show()

#fermer la connexion
connexion.close()
