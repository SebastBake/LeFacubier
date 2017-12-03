""" handles URL/request parsing, and routes to the response
"""
from . import APP
from .controller import controller


@APP.route("/")
@APP.route("/index.html")
def index():
    """Index Page
    """
    return controller.home_page()


@APP.route('/register', methods=('GET', ))
def register():
    """Login Page
    """
    return controller.register_page()


@APP.route('/login', methods=('POST', ))
def login():
    """ login user """
    return controller.login_submission()


@APP.route('/signup', methods=('POST', ))
def signup():
    """ signup user """
    return controller.signup_submission()


@APP.route('/logout', methods=('GET', ))
def logout():
    """ logout user """
    return controller.logout_submission()


@APP.route('/dash', methods=('GET', ))
def dash():
    """user dashboard"""
    return controller.in_progress_page("Dash")


@APP.route('/settings', methods=('GET', ))
def settings():
    """user settings"""
    return controller.in_progress_page("Settings")
