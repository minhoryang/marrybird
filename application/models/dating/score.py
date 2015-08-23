"""."""
__author__ = 'minhoryang'

from sqlalchemy_enum34 import EnumType as _EnumType

from .. import db
from .tier import TierType

class EnumType(_EnumType):
    def copy(self, *args, **kargs):
        if 'schema' in kargs:
            kargs.pop('schema')
        return super(__class__, self).copy(*args, **kargs)


# XXX : Need to be close with Record.DB
class Score(db.Model):
    __bind_key__ = "score"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)

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