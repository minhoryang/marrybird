from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(200))
	#gender
	created_at = db.Column(db.DateTime, default=datetime.now)

	def __setattr__(self, name, value):
		if name == 'password':
			value = generate_password_hash(value)
		super(User, self).__setattr__(name, value)

	def check_password(self, password):
		return check_password_hash(self.password, password)

