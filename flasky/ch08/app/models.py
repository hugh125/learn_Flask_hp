# -*- conding:utf-8 -*-

from werkzeug.security import \
	generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Role(db.Model):
	__tablename__ = 'roles'     # 数据库里的表名
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	#users = db.relationship('User', backref='role')

	def __repr__(self):
		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'     # 数据库里的表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    # myPwd = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        print('----------------------', password)
        print()
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.session.add(self)
        return True

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
