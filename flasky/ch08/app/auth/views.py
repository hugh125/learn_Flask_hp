from flask import render_template, redirect, request, url_for, flash
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user
from flask_login import logout_user, login_required
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        print()
        print(form.email.data)
        print(user)
        print(form.password.data)
        print(user.password)
        print()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or passord')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print()
    print(__file__, form.email.data)
    print(__file__, form.username.data)
    print(__file__, form.password.data)
    print(__file__, form.validate_on_submit())
    UserList = User.query.all()
    for u in UserList:
        print(u.username, u.email, u.password, u.password_hash)
        if u.password_hash is None:
            db.session.delete(u)
        db.session.commit()
    print()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you email.')
        #flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)