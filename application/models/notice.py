"""will served with dating.response"""

__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from . import db


class Notice(db.Model):
    __bind_key__ = "notice"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))
    notice = db.Column(db.String(200))
    photo_url = db.Column(db.String(50))

    def jsonify(self):
        return {
            'message': self.notice,
            'photo_url': self.photo_url,
            'datetime': self.created_at,
        }

def init(api, jwt):
    pass