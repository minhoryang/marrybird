__author__ = 'minhoryang'

from datetime import datetime

from .. import db

class Progress(db.Model):
    """ User A loves User B."""
    __bind_key__ = "progress"

    id = db.Column(db.Integer, primary_key=True)
    response_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    A = db.Column(db.String(20))  # TODO: Integer will be faster.
    B = db.Column(db.String(20))

    @staticmethod
    def SearchWhoLovesMe(b_username):
        found = Progress.query.filter(Progress.B == b_username).all()
        return [user.A for user in found]

    @staticmethod
    def SearchMeLovesWho(a_username):
        found = Progress.query.filter(Progress.A == a_username).all()
        return [user.B for user in found]

    @staticmethod
    def SearchHeLovesSheOrNot(list_a, list_b):
        HeLovesShe = []
        AOnlyLoveB = []
        BOnlyLoveA = []
        for i in list_a:
            if i in list_b:
                HeLovesShe.append(i)
            else:
                AOnlyLoveB.append(i)
        for i in list_b:
            if not i in HeLovesShe:
                BOnlyLoveA.append(i)
        return HeLovesShe, AOnlyLoveB, BOnlyLoveA

    @staticmethod
    def Love(a_username, b_username, response_id):
        lover = Progress()
        lover.A = a_username
        lover.B = b_username
        lover.response_id = response_id
        return lover

    @staticmethod
    def Hate(i, you):
        found = __class__.query.filter(
            __class__.A == you,
            __class__.B == i,
        ).first()
        if found:
            return found
        return None


def init(api, jwt):
    pass