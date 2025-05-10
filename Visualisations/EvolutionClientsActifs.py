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

#Évolution des clients actifs

df = pd.read_sql("""
SELECT DATE_FORMAT(rental_date, '%Y-%m') AS month, COUNT(DISTINCT customer_id) AS clients
FROM rental
GROUP BY month
ORDER BY month
""", engine)

df.plot(x="month", y="clients", kind="line", title="Clients actifs par mois", color ="orange")
print("Récapitulatif des clients actifs")
print(df)
plt.show()



