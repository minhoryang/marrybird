"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from .. import db

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

    school_score = db.Column(db.Float, nullable=False)
    work_score = db.Column(db.Float, nullable=False)
    attraction_score = db.Column(db.Float, nullable=False)

def init(api, jwt):
    pass  # XXX: No plan