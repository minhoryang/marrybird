"""."""
__author__ = 'minhoryang'

from .. import db

class Review(db.Model):
    __bind_key__ = "review"

    id = db.Column(db.Integer, primary_key=True)

def init(api, jwt):
    pass