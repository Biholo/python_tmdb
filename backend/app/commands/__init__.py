
from .sync_database import download_and_extract_json
from .init_database import init_model_and_database

def register_commands(app):
    app.cli.add_command(download_and_extract_json)
    app.cli.add_command(init_model_and_database)


