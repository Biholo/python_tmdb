import os
import requests
import gzip
import json
from datetime import datetime, timedelta
import click
from flask.cli import with_appcontext
import pandas as pd
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import sessionmaker
from ..services.database import database

@click.command('sync-database-movies')
@with_appcontext
def download_and_extract_json():
    # Calcul de la date du fichier
    yesterday = datetime.now() - timedelta(1)
    date_str = yesterday.strftime('%m_%d_%Y')

    url = f"http://files.tmdb.org/p/exports/movie_ids_{date_str}.json.gz"
    
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    gz_file_path = os.path.join(data_dir, f'movie_ids_{date_str}.json.gz')
    json_file_path = os.path.join(data_dir, f'movie_ids_{date_str}.json')

    # Téléchargement du fichier si nécessaire
    if os.path.exists(gz_file_path):
        print(f"Le fichier {gz_file_path} existe déjà. Pas besoin de le télécharger.")
    else:
        response = requests.get(url)
        if response.status_code == 200:
            with open(gz_file_path, 'wb') as f:
                f.write(response.content)
            print(f"Fichier téléchargé et stocké à: {gz_file_path}")
        else:
            print(f"Erreur lors du téléchargement du fichier: {response.status_code}")
            return

    # Extraction du fichier si nécessaire
    if os.path.exists(json_file_path):
        print(f"Le fichier {json_file_path} existe déjà. Pas besoin de l'extraire.")
    else:
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(json_file_path, 'wb') as f_out:
                f_out.write(f_in.read())
        print(f"Fichier extrait à: {json_file_path}")

    # Chargement des données JSON dans un DataFrame
    movies_df = pd.read_json(json_file_path, lines=True)

    # Réinitialiser l'index du DataFrame et s'assurer qu'il ne contient pas d'index inutile
    movies_df = movies_df.reset_index(drop=True)

    batch_size = 10000
    num_batches = len(movies_df) // batch_size + 1

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = start_idx + batch_size
        batch_df = movies_df.iloc[start_idx:end_idx]

        if 'index' in batch_df.columns:
            batch_df = batch_df.drop(columns=['index'])

        print(f"Inserting batch {i+1}/{num_batches} into the database")
        try:
            database.load_dataframe_to_db(batch_df, 'movie')
        except Exception as e:
            print(f"Erreur lors de l'insertion du batch {i+1}/{num_batches} dans la table movie: {e}")

if __name__ == "__main__":
    download_and_extract_json()
