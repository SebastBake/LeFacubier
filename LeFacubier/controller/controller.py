"""This controller is the app-side facade"""
from flask import render_template, redirect, flash
from werkzeug.exceptions import Unauthorized, Conflict, Gone
from ..services import auth, messaging, notification, user_post, profile
from . import forms

def home_page():
    """returns the home page"""
    try:
        from flask import session
        s_id, s_key = (session[auth.SESSION_ID], session[auth.SESSION_KEY])
        username = auth.authenticate_session(s_id, s_key)
        return render_template('index.html', user=username)
    except (Unauthorized, Gone) as exception:
        flash(exception.description)
    except KeyError:
        pass
    return render_template('index.html', user=None)


def register_page():
    """returns the login/signup page"""
    try:
        from flask import session
        s_id, s_key = (session[auth.SESSION_ID], session[auth.SESSION_KEY])
        username = auth.authenticate_session(s_id, s_key)
        flash("Already logged in")
        return render_template('index.html', user=username)
    except (Unauthorized, Gone) as exception:
        flash(exception.description)
    except KeyError:
        pass
    login, signup = (forms.LoginForm(), forms.SignupForm())
    return render_template('who_are_you.html', loginform=login, signupform=signup)


def login_submission():
    """logs the user into the system"""
    form = forms.LoginForm()

    if not form.validate_on_submit():
        flash("Please correctly fill login form")
        forms.flash_errors(form)
        return redirect('/register')

    email, pwd = (form.email.data, form.password.data)

    try:
        session_auth = auth.create_session(email, pwd)
        from flask import session
        session.update(session_auth)
        return redirect('/dash')
    except Unauthorized:
        flash("Incorrect username or password")
        forms.flash_errors(form)
        return redirect('/register')


def logout_submission():
    """logs the user out of the system"""
    try:
        from flask import session
        s_id, s_key = (session[auth.SESSION_ID], session[auth.SESSION_KEY])
        auth.destroy_session(s_id, s_key)
        flash("bye!")
        return redirect('/')
    except Unauthorized:
        flash("You aren't logged in...")
        return render_template('index.html', user=None)


def signup_submission():
    """signs a user up for the service"""
    form = forms.SignupForm()

    if not form.validate_on_submit():
        flash("Please correctly fill signup form")
        forms.flash_errors(form)
        return redirect('/register')

    username, email, pwd = (form.username.data, form.email.data,
                            form.password.data)

    try:
        auth.create_user(username, email, pwd)
        session_auth = auth.create_session(email, pwd)
        from flask import session
        session.update(session_auth)
        return redirect('/dash')
    except Conflict as exception:
        flash(exception.description)
        forms.flash_errors(form)
        return redirect('/register')


def in_progress_page(pagename):
    """returns the in progress page page"""
    try:
        from flask import session
        s_id, s_key = (session[auth.SESSION_ID], session[auth.SESSION_KEY])
        username = auth.authenticate_session(s_id, s_key)
        return render_template('in_progress.html', user=username, pagename=pagename)
    except (Unauthorized, Gone) as exception:
        flash(exception.description)
    except KeyError:
        pass
    return render_template('in_progress.html', user=None, pagename=pagename)
