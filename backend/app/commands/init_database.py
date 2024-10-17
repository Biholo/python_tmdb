import click
from flask.cli import with_appcontext
from ..services.database import database

@click.command('init-database')
@with_appcontext
def init_model_and_database():
    """
    Supprime toutes les tables existantes et les recrée à partir des modèles.
    """
    database.reset_db()
    print("Base de données réinitialisée avec succès.")

