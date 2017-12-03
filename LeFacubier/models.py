""" Database models """
from . import DB


class User(DB.Model):
    """ Represents a user
    """

    USERNAME_LEN = 20
    EMAIL_LEN = 345
    PASSWORD_LEN = 100

    __tablename__ = 'users'

    id = DB.Column(DB.Integer, DB.Sequence('user_id_seq'), primary_key=True)
    username = DB.Column(DB.String(USERNAME_LEN), unique=True, nullable=False)
    email = DB.Column(DB.String(EMAIL_LEN), unique=True, nullable=False)
    password = DB.Column(DB.LargeBinary(PASSWORD_LEN), unique=False, nullable=False)

    def __repr__(self):
        stuff = (self.email, self.username, self.password)
        return '<User email: {}, username: {}, password: {}>'.format(*stuff)


class UserSession(DB.Model):
    """ Represents a user session
    """

    KEY_LEN = 100

    __tablename__ = 'sessions'

    id = DB.Column(DB.Integer, DB.Sequence('session_id_seq'), primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('users.id'), nullable=False)
    key = DB.Column(DB.LargeBinary(KEY_LEN), unique=False, nullable=False)
    expiry = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return '<UserSession user_id: {}>'.format(self.user_id)
    