"""Responsible for handling user authentication and authorisation"""
import string
import random
import datetime
import bcrypt
from werkzeug.exceptions import Unauthorized, Conflict, Gone
from ..models import User, UserSession, DB

SESSION_KEY = 'SESSION_KEY'
SESSION_ID = 'SESSION_ID'
SESSION_LIFETIME = datetime.timedelta(days=30)

def create_user(username, email, password):
    """Registers a new user"""

    username_taken = User.query.filter_by(username=username).first()
    email_taken = User.query.filter_by(email=email).first()

    if username_taken:
        raise Conflict('Username already taken')

    if email_taken:
        raise Conflict('Email already taken')

    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    user = User(email=email, username=username, password=hashed_password)

    DB.session.add(user)
    DB.session.commit()
    DB.session.flush()

def create_session(email, password):
    """Authenticate a user"""
    user = User.query.filter_by(email=email).first()

    if not user:
        raise Unauthorized("User not found")

    if not bcrypt.checkpw(password.encode('utf8'), user.password):
        raise Unauthorized("Incorrect password")

    key = _gen_key()
    hashed_key = bcrypt.hashpw(key.encode('utf8'), bcrypt.gensalt())

    user_session = UserSession(user_id=user.id, key=hashed_key,
                               expiry=_gen_expiry())

    DB.session.add(user_session)
    DB.session.commit()
    DB.session.flush()

    return {SESSION_KEY: key, SESSION_ID: user_session.id}

def destroy_session(s_id, s_key):
    """Logout a user"""
    session = UserSession.query.filter_by(id=s_id).first()

    if not session:
        raise Unauthorized("Session not found")

    if not bcrypt.checkpw(s_key.encode('utf8'), session.key):
        raise Unauthorized("Invalid session key")

    DB.session.delete(session)
    DB.session.commit()


def authenticate_session(s_id, s_key):
    """Authenticates a user request using a cookie"""

    session = UserSession.query.filter_by(id=s_id).first()

    if not session:
        raise Unauthorized("Session not found")

    if not bcrypt.checkpw(s_key.encode('utf8'), session.key):
        DB.session.delete(session)
        DB.session.commit()
        raise Unauthorized("Invalid session key")

    if datetime.datetime.today().timestamp() > session.expiry:
        DB.session.delete(session)
        DB.session.commit()
        raise Unauthorized("Session expired")

    user = User.query.filter_by(id=session.user_id).first()
    if not user:
        DB.session.delete(session)
        DB.session.commit()
        raise Gone("User is missing (possibly deleted)")

    return user.username


def _gen_expiry():
    """ returns an expiry date """
    return (datetime.datetime.today() + SESSION_LIFETIME).timestamp()


def _gen_key():
    """ returns a random key """
    char = string.digits + string.ascii_letters
    return ''.join(random.choice(char) for i in range(UserSession.KEY_LEN))
