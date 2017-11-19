"""routes
"""
import time
from flask import render_template, redirect, flash, request, session
from LeFacubier import APP
from LeFacubier.forms import LoginForm, SignupForm
from LeFacubier.models import User, UserSession

@APP.route("/")
@APP.route("/index.html")
def index():
    """Index Page
    """
    try:
        user = UserSession.get_user_from_session()
        print(user)
        renderuser = {
            'email': user.email,
            'username': user.username,
            'password': user.password
        }
        return render_template('index.html', user=renderuser)
    except Exception:
        renderuser = {
            'email': 'not logged in',
            'username': 'none',
            'password': 'none'
        }
    return render_template('index.html', user=renderuser)

@APP.route('/login-or-signup', methods=('GET',))
def login_or_signup():
    """Login Page
    """
    return render_template(
        'login.html',
        loginform=LoginForm(),
        signupform=SignupForm())

@APP.route('/login', methods=('POST',))
def login():
    """Login Page
    """
    loginform = LoginForm()

    if loginform.validate_on_submit():

        new_user = User.from_request(request)
        old_user = User.get_by_email(new_user.email)

        if old_user.password != new_user.password:
            flash("incorrect username or password")
            return redirect('/login-or-signup')
        else:
            print(UserSession.new(old_user.id))
            flash("Logged in")
            return redirect('/')
    else:
        flash("Please correctly fill login form")
        return redirect('/login-or-signup')

@APP.route('/signup', methods=('POST',))
def signup():
    """ signup """
    signupform = SignupForm()

    if signupform.validate_on_submit():

        new_user = User.from_request(request)
        print("sign up: " + new_user.__repr__())

        if User.get_by_username(new_user.username):
            flash("Username already taken")
            return redirect('/login-or-signup')
        elif User.get_by_email(new_user.email):
            flash("Email already taken")
            return redirect('/login-or-signup')
        else:
            new_user = User.submit(new_user)
            flash("Signed up as " + new_user.username)
            UserSession.new(new_user.id)
            return redirect('/')
    else:
        flash("Please correctly fill signup form")
        return redirect('/login-or-signup')
