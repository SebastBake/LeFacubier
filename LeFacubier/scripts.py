"""
    This module contains flask cli scripts for performing various tasks.
    To run a task
"""
from LeFacubier import APP, DB

DB_URL = APP.config['SQLALCHEMY_DATABASE_URI']

@APP.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database
    from sqlalchemy_utils import drop_database

    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    DB.create_all()
    print('Shiny!')
