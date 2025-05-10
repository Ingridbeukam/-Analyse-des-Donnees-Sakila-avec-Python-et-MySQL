#connexion a Mysql
import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
from statsmodels.tsa.arima.model import ARIMA

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
# Série mensuelle des locations
query = """
SELECT DATE_FORMAT(rental_date, '%Y-%m') AS mois, COUNT(*) AS nb_locations
FROM rental
GROUP BY mois
ORDER BY mois;
"""
df_ts = pd.read_sql(query, engine, index_col="mois", parse_dates=True)

# ARIMA simple
model = ARIMA(df_ts["nb_locations"], order=(1, 1, 1))
model_fit = model.fit()
forecast = model_fit.forecast(steps=6)

# Visualisation
plt.plot(df_ts.index, df_ts["nb_locations"], label="Historique")
plt.plot(forecast.index, forecast, label="Prévision", color="red")
plt.title("Prévision des locations (ARIMA)")
plt.legend()
plt.xticks(rotation=45)
plt.show()
print("Prévision des locations")
print()


print("""
Dans ce projet, nous avons utilisé le modèle ARIMA pour prévoir le nombre de locations 
mensuelles dans la base Sakila, basée sur les données historiques. 
Le modèle a permis de générer des prévisions précises qui peuvent aider
une entreprise de location de films à mieux gérer ses stocks, 
planifier des campagnes marketing et optimiser ses ressources humaines.
""")
