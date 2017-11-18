"""A brutalist facebook project"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)
APP.config.from_object('config')
DB = SQLAlchemy(APP)

# import app modules at the bottom to prevent circular import error
from LeFacubier import models, routes, scripts
