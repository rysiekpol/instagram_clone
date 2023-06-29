from flask import redirect, url_for, flash, request, render_template
from flask_login import login_user, current_user

from werkzeug.urls import url_parse
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


def authenticate_user():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
def validate_login_form(form: LoginForm):
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    
def validate_registration_form(form: RegistrationForm):
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))