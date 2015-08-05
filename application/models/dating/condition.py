__author__ = 'minhoryang'

from datetime import datetime
from .. import db

class Condition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    added_at = db.Column(db.DateTime, default=datetime.now)

    # conditions
    conditions_json = db.Column(db.String(200))  # json)) beauty>>,graduatedschool>3,age<30,...

    @staticmethod
    def get_latest_condition_by_user(username):
        latest = Condition.query.filter(
            Condition.username == username
        ).order_by(
            Condition.added_at.desc()
        ).first()
        return latest

def init(api, jwt):
    pass  # done. No RestAPI.
