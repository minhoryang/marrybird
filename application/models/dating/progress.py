__author__ = 'minhoryang'

from .. import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def init(api, jwt):
    pass