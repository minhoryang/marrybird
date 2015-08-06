__author__ = 'minhoryang'

from datetime import datetime

from .. import db

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    A = db.Column(db.String(20))
    B = db.Column(db.String(20))

    @staticmethod
    def SearchWhoLovesMe(b_username):
        found = Progress.query.filter(Progress.B == b_username)
        return found

    @staticmethod
    def SearchMeLovesWho(a_username):
        found = Progress.query.filter(Progress.A == a_username)
        return found

    @staticmethod
    def Love(a_username, b_username):
        return None

def init(api, jwt):
    pass