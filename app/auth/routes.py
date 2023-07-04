from flask import render_template, redirect, url_for
from flask_login import logout_user

from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.auth.services import authenticate_user, validate_login_form, validate_registration_form


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if (auth := authenticate_user()):
        return auth
    form = LoginForm()
    if (validate := validate_login_form(form)):
        return validate
    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET','POST'])
def register():
    if (auth := authenticate_user()):
        return auth
    form = RegistrationForm()
    if (validate := validate_registration_form(form)):
        return validate
    
    return render_template('auth/register.html', title='Register',
                           form=form)
