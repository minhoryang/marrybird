__author__ = 'minhoryang'

import enum
from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr


from .. import db

class Tier(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # db.ForeignKey('score.id'), 


class TierType(enum.Enum):
    aA = "aA"
    aB = "aB"
    aC = "aC"
    bB = "bB"
    bC = "bC"
    cC = "cC"

    @staticmethod
    def getAvailbleTiers(cls):
        pass  # TODO


def init(api, jwt):
    pass  # XXX: No plan