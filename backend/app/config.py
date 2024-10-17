import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')  # Clé secrète pour Flask (sessions, etc.)
    TMDB_API_KEY = os.getenv('TMDB_API_KEY')
    TMDB_SECRET_KEY = os.getenv('TMDB_SECRET_KEY')
    DEBUG = True
