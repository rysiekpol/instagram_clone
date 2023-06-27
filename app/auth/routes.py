from flask import render_template, redirect, url_for
from flask_login import logout_user

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.services import *


@bp.route('/login', methods=['GET', 'POST'])
def login():
    auth = authenticate_user()
    if auth:
        return auth
    form = LoginForm()
    validate = validate_login_form(form)
    if validate:
        return validate
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    auth = authenticate_user()
    if auth:
        return auth
    form = RegistrationForm()
    validate = validate_registration_form(form)
    if validate:
        return validate
    
    return render_template('auth/register.html', title='Register',
                           form=form)
