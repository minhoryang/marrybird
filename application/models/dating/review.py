"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from .. import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def init(api, jwt):
    pass