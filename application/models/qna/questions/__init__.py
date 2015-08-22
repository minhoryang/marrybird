__author__ = 'minhoryang'

from ... import db

from sqlalchemy_utils import JSONType

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asd = db.Column(JSONType)

def init(api, jwt):
    pass