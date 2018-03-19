from flask import render_template, redirect, request, url_for, flash
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from ..email import send_email
import sys

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
    UserList = User.query.all()
    for u in UserList:
        print("{'%s', '%s', '%s'}" % (u.username, u.email, u.myPwd))
        #print("{username = '%s', email = '%s', password = '%s'}"              % (u.username, u.email, u.myPwd))
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

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirm you account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expried')
    return  redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user,token=token)
    flash('A new confirmation email hash been sent to you by email.')
    return redirect(url_for('auth.unconfirmed'))
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    print(request.blueprint)
    print(request.endpoint)
    print(request.endpoint[:5])
    # print(current_user.confirmed)
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth' \
            and request.endpoint != 'static':
        #return redirect(url_for('main.index'))
        print(url_for('auth.unconfirmed'))
        #return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    print('line:', sys._getframe().f_lineno)
    print('current_user.is_anonymous:', current_user.is_anonymous)
    print('current_user.confirmed:', current_user.confirmed)
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')