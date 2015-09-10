"""stores the description of the result from Question Books."""

__author__ = 'minhoryang'

from .. import db


class ResultBook(db.Model):
    __bind_key__ = "resultbook"

    id = db.Column(db.Integer, primary_key=True)
    question_book_id = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=True)


def init(api, jwt):
    pass

def module_init(api, jwt, namespace):
    pass