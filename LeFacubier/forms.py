"""form
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length
from LeFacubier.models import User

EMAIL = StringField('email', validators=[
    DataRequired(message="Email must not be empty"),
    Email(message="Email must be a valid email address"),
    Length(
        min=5,
        max=User.EMAIL_MAX_LEN,
        message="Email length must be between %(min)d and %(max)d characters")])

USERNAME = StringField('username', validators=[
    DataRequired(),
    Length(
        min=1,
        max=User.USERNAME_MAX_LEN,
        message="Username length must be between %(min)d and %(max)d characters")])

PASSWORD = PasswordField('Password', validators=[
    DataRequired(),
    Length(
        min=6,
        message="Email length must be at least %(min)d characters")])

class LoginForm(FlaskForm):
    email = EMAIL
    password = PASSWORD

class SignupForm(FlaskForm):
    email = EMAIL
    username = USERNAME
    password = PASSWORD
