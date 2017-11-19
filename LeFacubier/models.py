""" Models.py
"""
from LeFacubier import DB
import string
import random
import datetime

#DB.Model is a base class
class User(DB.Model):
    """ Represents a user
    """

    USERNAME_MAX_LEN = 20
    EMAIL_MAX_LEN = 345
    PASSWORD_MAX_LEN = 300

    __tablename__ = 'users'

    id = DB.Column(
        DB.Integer,
        DB.Sequence('user_id_seq'),
        primary_key=True)

    username = DB.Column(
        DB.String(USERNAME_MAX_LEN),
        unique=True,
        nullable=False)

    email = DB.Column(
        DB.String(EMAIL_MAX_LEN),
        unique=True,
        nullable=False)

    password = DB.Column(
        DB.String(PASSWORD_MAX_LEN),
        unique=False,
        nullable=False)

    @staticmethod
    def from_request(req):
        """ generate a user from a request
        """
        return User(
            password=req.form['password'],
            email=req.form['email'])

    @staticmethod
    def submit(user):
        """ Add a new user into the database
        """
        DB.session.add(user)
        DB.session.commit()
        DB.session.flush()
        return user

    @staticmethod
    def get_by_email(email):
        """ returns a list of users with the username """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_username(username):
        """ returns a list of users with the username """
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User email: {}, username: {}, password: {}>'.format(
            self.email,
            self.username,
            self.password)

class UserSession(DB.Model):
    """ Represents a user session
    """

    __tablename__ = 'sessions'

    SESSION_CHECKSTRING_KEY = 'SESSION_CHECKSTRING'
    SESSION_ID_KEY = 'SESSION_ID'
    CHECKSTRING_LEN = 240
    EXPIRATION_TIME = datetime.timedelta(days=30)

    id = DB.Column(DB.Integer, DB.Sequence('session_id_seq'), primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=False)
    checkstring = DB.Column(DB.String(CHECKSTRING_LEN), unique=False, nullable=False)
    expiry = DB.Column(DB.Integer, nullable=False)

    @staticmethod
    def new(user_id):
        """ returns a new foobar """
        user_session = UserSession(
            user_id=user_id,
            checkstring=UserSession.generate_checkstring(),
            expiry=UserSession.generate_expiry())

        DB.session.add(user_session)
        DB.session.commit()
        DB.session.flush()

        from flask import session
        session[UserSession.SESSION_CHECKSTRING_KEY] = user_session.checkstring
        session[UserSession.SESSION_ID_KEY] = user_session.id
        return user_session

    @staticmethod
    def generate_checkstring():
        """ returns a checkstring """
        chars = string.ascii_lowercase + string.ascii_uppercase + '0123456789'
        return ''.join(random.choice(chars) for i in range(UserSession.CHECKSTRING_LEN))

    @staticmethod
    def generate_expiry():
        """ returns an expiry date """
        return (datetime.datetime.today() + UserSession.EXPIRATION_TIME).timestamp()

    @staticmethod
    def get_user_from_session():
        """ logs a user into the system using a session from cookie """

        from flask import session
        checkstring = session[UserSession.SESSION_CHECKSTRING_KEY]
        session_id = session[UserSession.SESSION_ID_KEY]

        user_session = UserSession.query.filter_by(id=session_id, checkstring=checkstring).first()
        print("User session = " + user_session.__repr__())
        user = None

        if user_session:
            user = User.query.filter_by(id=user_session.user_id).first()

        if user: 
            return user

        print("no user foud from session")
        raise Exception("couldn't find user")
    
    def __repr__(self):
        return '<UserSession user_id: {}>'.format(
            self.user_id)
