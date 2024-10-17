from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

host = 'mysql-transport.alwaysdata.net'
user = 'transport'
password = 'kiks2002'
db = 'transport_tmdb'

Base = declarative_base()

class Database:
    def __init__(self, host, user, password, db_name):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.db_name}')
            print("Connexion à la base de données réussie")
        except Exception as e:
            print(f"Erreur lors de la connexion à la base de données: {e}")

    def ensure_connection(self):
        if self.engine is None:
            self.connect()
            if self.engine is None:
                raise Exception("La connexion à la base de données n'est pas établie.")

    def load_dataframe_to_db(self, dataframe, table_name):
        self.ensure_connection()
        try:
            print(f"Insertion des données dans la table {table_name}...")
            dataframe[['adult', 'id', 'original_title', 'popularity', 'video']].to_sql(
                table_name, con=self.engine, if_exists='append', chunksize=500, index=False
            )
            print(f"Les données ont été insérées dans la table {table_name}.")
        except SQLAlchemyError as e:
            print(f"Erreur lors de l'insertion des données dans la table {table_name}: {e}")

    def execute_query(self, query, params=None):
        """Exécuter une requête SQL (INSERT, UPDATE, DELETE)"""
        self.ensure_connection()
        try:
            with self.engine.connect() as connection:
                connection.execute(text(query), params)
                connection.commit()
                print("Requête exécutée avec succès")
        except SQLAlchemyError as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")

    def fetch_all(self, query, params=None):
        """Exécuter une requête SELECT et retourner tous les résultats"""
        self.ensure_connection()
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query), params)
                rows = result.fetchall()
                return rows
        except SQLAlchemyError as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            return []

# Exécution principale
database = Database(host, user, password, db)
database.connect()
