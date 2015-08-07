__author__ = 'minhoryang'

from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr

from .. import db

class Met(db.Model):
    # AbstractConcreteBase
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    """@declared_attr
    def __mapper_args__(cls):
        return {'polymorphic_identity': cls.__name__,
                'concrete': True} if cls.__name__ != "Met" else {}"""

class Met_Rejected(Met):
    id = db.Column(db.Integer, db.ForeignKey('met.id'), primary_key=True)

class Met_Accepted(Met):
    id = db.Column(db.Integer, db.ForeignKey('met.id'), primary_key=True)

class Met_NotResponsed(Met):
    id = db.Column(db.Integer, db.ForeignKey('met.id'), primary_key=True)


def init(api, jwt):
    pass