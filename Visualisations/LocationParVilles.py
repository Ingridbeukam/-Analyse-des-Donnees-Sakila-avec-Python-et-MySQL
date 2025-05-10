#connexion a Mysql
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

print("connexion reussie")

#. Locations par ville
df = pd.read_sql("""
SELECT city, COUNT(*) AS total
FROM rental
JOIN customer USING(customer_id)
JOIN address USING(address_id)
JOIN city USING(city_id)
GROUP BY city
ORDER BY total DESC
LIMIT 15
""", engine)

df.sort_values("total").plot(kind="bar", x="city", y="total", title="Locations par ville", color="violet")
plt.xticks(rotation=45)
print("Total de location par ville")
print(df)
plt.show()

