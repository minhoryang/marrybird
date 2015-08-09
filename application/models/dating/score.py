"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_enum34 import EnumType

from .. import db
from .tier import TierType


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)

    school_score = db.Column(db.Float, nullable=False)
    work_score = db.Column(db.Float, nullable=False)
    attraction_score = db.Column(db.Float, nullable=False)

    tier = db.Column(db.String(2), nullable=False)
    tierr = db.Column(EnumType(TierType))

    def __setattr__(self, key, value):
        #old = self.tierr
        super(Score, self).__setattr__(key, value)
        if key is 'tier':
            self.tierr = TierType(value)


def init(api, jwt):
    pass  # XXX: No plan