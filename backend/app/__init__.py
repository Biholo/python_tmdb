from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes.routes import main
from .commands import register_commands
from .services.database import database

# Initialiser l'application Flask
def create_app():
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(Config)
    
    # Définir les origines autorisées
    allowed_origins = [
        "http://example.com",
        "http://localhost:5173",
        "http://localhost:5174",

    ]

    # Appliquer CORS à l'application
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    # Importer et enregistrer les routes
    app.register_blueprint(main)
    
    # Importer et enregistrer les commandes
    register_commands(app)

    # Initialiser la base de données
    database.connect()
    
    return app
