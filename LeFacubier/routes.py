"""routes
"""
from flask import render_template, redirect, flash, request
from LeFacubier import APP, DB
from LeFacubier.forms import LoginForm, SignupForm
from LeFacubier.models import User

@APP.route("/")
@APP.route("/index.html")
def index():
    """Index Page
    """

    defaultuser = {
        'user': 'none',
        'username': 'none',
        'password': 'none'
    }
    return render_template('index.html', user=defaultuser)

@APP.route('/login-or-signup', methods=('GET',))
def login_or_signup():
    """Login Page
    """

    loginform = LoginForm()
    signupform = SignupForm()

    return render_template(
        'login.html',
        loginform=loginform,
        signupform=signupform
        )

@APP.route('/login', methods=('POST',))
def login():
    """Login Page
    """

    loginform = LoginForm()

    if loginform.validate_on_submit():
        new_user = User(username=request.form['email'], password=request.form['password'])
        APP.logger.warn("login: usrnme={} with pwd={}".format(new_user.username, new_user.password))
        old_user = User.query.filter_by(username=new_user.username)
        
        if old_user.password != new_user.password:
            flash("incorrect username or password")
            response = redirect('/login-or-signup')
        else:
            response = redirect('/')

    else:
        flash("Please correctly fill login form")
        response = redirect('/login-or-signup')

    return response

@APP.route('/signup', methods=('POST',))
def signup():
    """signup Page
    """

    signupform = SignupForm()

    if signupform.validate_on_submit():
        new_user = User(username=request.form['email'], password=request.form['password'])
        if not User.query.filter_by(username=new_user.username):
            DB.session.add(new_user)
            DB.session.commit()
            APP.logger.warn("sign up: usrnme={} with pwd={}".format(new_user.username, new_user.password))
            response = redirect('/')
        else:
            flash("email already taken")
            response = redirect('/login-or-signup')

    else:
        flash("Please correctly fill signup form")
        response = redirect('/login-or-signup')

    return response
