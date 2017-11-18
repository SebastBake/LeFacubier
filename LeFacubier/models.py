"""
    Models.py
"""
from LeFacubier import DB

#DB.Model is a base class
class User(DB.Model):
    """
        Represents a user
    """

    __tablename__ = 'users'

    id = DB.Column(DB.Integer, DB.Sequence('user_id_seq'), primary_key=True)
    username = DB.Column(DB.String(50), unique=False)
    password = DB.Column(DB.String(50), unique=False)

    @staticmethod
    def user_from_request(req):
        """ generate a user from a request
        """
        try:
            return User(username=req.form['email'], password=req.form['password'])
        except:
            raise ModelConstructionException

    def __repr__(self):
        return '<User id:{:d} , username:{} , password:{}>'.format(id, username, password)

class ModelConstructionException(Exception):
    pass
