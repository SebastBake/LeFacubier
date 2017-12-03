"""Responsible for generating html forms and processing he responses"""
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from ..models import User

EMAIL = StringField('Email', validators=[
    validators.DataRequired(message="Email must not be empty"),
    validators.Email(message="Email must be a valid email address")])

USERNAME = StringField('Username', validators=[
    validators.DataRequired(message="Username must not be empty"),
    validators.Length(
        max=User.USERNAME_LEN,
        message="Username length must be less than %(max)d characters")])

PASSWORD = PasswordField('Password', validators=[
    validators.DataRequired(message="Password must not be empty"),
    validators.Length(
        min=6,
        message="Password length must be at least %(min)d characters")])


class LoginForm(FlaskForm):
    """ Represents the login form """
    email = EMAIL
    password = PASSWORD


class SignupForm(FlaskForm):
    """ Represents the signup form """
    email = EMAIL
    username = USERNAME
    password = PASSWORD


def flash_errors(form):
    for error_set in form.errors.items():
        for error in error_set[1]:
            print(error)
            flash(error)
