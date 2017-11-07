"""This module does blah blah."""
from flask import Flask

APP = Flask(__name__)

@APP.route("/")
def main():
    'this is my docstring'
    return "Welcome!"
