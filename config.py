"""Config file"""
import os
import sys

try:
    # Database url constructed from environment variables
    POSTGRES = {
        'user': os.environ['DB_USER'],
        'pw': os.environ['DB_PW'],
        'db': os.environ['DB'],
        'host': os.environ['DB_HOST'],
        'port': os.environ['DB_PORT'],
    }

    # Token used to validate form
    SECRET_KEY = os.environ['FORM_SECRET_KEY']

except KeyError as exception:
    print(exception)
    print("Set the environment variables.")
    sys.exit(1)

SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{pw}@{host}:{port}/{db}'.format(**POSTGRES)

# Suppress a depreciation warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
