"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from .. import db

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #TODO : TEST
    isDone = db.Column(db.Boolean)

def init(api, jwt):
    pass