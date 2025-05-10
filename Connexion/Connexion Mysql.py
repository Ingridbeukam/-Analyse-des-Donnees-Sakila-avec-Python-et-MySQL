#connexion a Mysql
import mysql.connector
from dotenv import load_dotenv
import os
import pandas as pd

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


