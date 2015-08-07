__author__ = 'minhoryang'

from datetime import datetime

from .. import db

class Progress(db.Model):
    """ User A loves User B."""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    A = db.Column(db.String(20))  # TODO: Integer will be faster.
    B = db.Column(db.String(20))

    @staticmethod
    def SearchWhoLovesMe(b_username):
        found = Progress.query.filter(Progress.B == b_username)
        return [user.A for user in found]

    @staticmethod
    def SearchMeLovesWho(a_username):
        found = Progress.query.filter(Progress.A == a_username)
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
    def Love(a_username, b_username):
        lover = Progress()
        lover.A = a_username
        lover.B = b_username
        db.session.add(lover)
        db.session.commit()


def init(api, jwt):
    pass