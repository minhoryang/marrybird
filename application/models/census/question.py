"""stores the various kinds of the Question."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime
from json import loads

from flask.ext.restplus import Resource, fields
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy_utils import ScalarListType

from .. import db


class Question(db.Model):
    __bind_key__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(200))

    # XXX : If None -> Essay Answer Needed!
    expected_answers = db.Column(ScalarListType(), nullable=True)
    json = db.Column(db.String(200), nullable=True)
    is_Multiple_Answer_Available = db.Column(db.Boolean, nullable=False)

    @hybrid_property
    def is_Essay_Answer_Needed(self):
        return self.expected_answers == None

    def __setattr__(self, key, value):
        if key == "json" and value:
            super(__class__, self).__setattr__("expected_answers", loads(value.replace("'", '"')))
            return
        super(__class__, self).__setattr__(key, value)

    def jsonify(self):
        return {
            'question': self.question,
            'is_Essay_Answer_Needed': self.is_Essay_Answer_Needed,
            'is_Multiple_Answer_Available': self.is_Multiple_Answer_Available,
            'expected_answers': self.expected_answers,
        }


class QuestionBook(db.Model):
    __bind_key__ = "questionbook"

    id = db.Column(db.Integer, primary_key=True)

    # front page
    title = db.Column(db.String(50))
    photo_url = db.Column(db.String(50))
    brief_description = db.Column(db.String(50))

    # details
    description = db.Column(db.String(200))

    # -delegated
    questions = db.Column(ScalarListType(int), default=[])
    num_of_questions = db.Column(db.Integer, default=0)

    def __setattr__(self, key, value):
        if key in ["questions", "num_of_questions"] and value:
            super(__class__, self).__setattr__(
                "questions",
                [
                    i.id
                    for i in Question.query.filter(
                        Question.book_id == self.id,
                    ).order_by(
                        Question.id.asc(),
                    ).all()
                ]
            )
            super(__class__, self).__setattr__(
                "num_of_questions",
                len(self.questions)
            )
            return  # delegated from below
        super(__class__, self).__setattr__(key, value)

    @staticmethod
    def getQuestionBooks():
        return __class__.query.all()

    @staticmethod
    def get(id):
        return __class__.query.get(id)

    def jsonify(self):
        return {
            'title': self.title,
            'photo_url': self.photo_url,
            'brief_description': self.brief_description,
            'description': self.description,
        }


def init(api, jwt):
    pass


def module_init(api, jwt, namespace):
    pass
