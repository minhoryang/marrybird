"""."""
__author__ = 'minhoryang'

from .. import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def init(api, jwt):
    pass