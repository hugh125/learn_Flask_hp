# -*- conding:utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import \
	generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# class Role(db.Model):
# 	__tablename__ = 'roles'	# 数据库里的表名
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(64), unique=True)
# 	#users = db.relationship('User', backref='role')
# 	#role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
#
# 	def __repr__(self):
# 		return '<Role %r>' % self.name

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	#role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	def __repr__(self):
		return '<User %r>' % self.username
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return  check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

if __name__ == '__main__':
	pass