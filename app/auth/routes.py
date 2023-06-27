from flask import render_template, redirect, url_for
from flask_login import logout_user

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.services import *


@bp.route('/login', methods=['GET', 'POST'])
def login():
    authenticate_user()
    form = LoginForm()
    validate_login_form(form)
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    authenticate_user()
    form = RegistrationForm()
    validate_registration_form(form)
    return render_template('auth/register.html', title='Register',
                           form=form)
