"""stores the various kinds of the Question."""

__author__ = 'minhoryang'

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
    isEssayAnswerNeeded = column_property(expected_answers == None)
    isMultipleAnswerAvailable = db.Column(db.Boolean)


class QuestionBook(db.Model):
    __bind_key__ = "questionbook"

    id = db.Column(db.Integer, primary_key=True)

    # front page
    title = db.Column(db.String(50))
    photo_url = db.Column(db.String(50))
    brief_description = db.Column(db.String(50))

    # details
    description = db.Column(db.String(200))
    questions = db.Column(ScalarListType(int), nullable=False)

    # -delegated
    num_of_questions = db.Column(db.Integer)

    def __setattr__(self, key, value):
        if key == "num_of_questions" and value:
            return  # delegated from below
        elif key == "questions" and value:
            super(__class__, self).__setattr__(
                "num_of_questions",
                len(self.questions)
            )
            super(__class__, self).__setattr__(key, value)
        else:
            super(__class__, self).__setattr__(key, value)

    def getQuestions(self):
        return Question.query.filter(
            Question.book_id == self.id,
        ).order_by(
            Question.id.asc()
        ).all()


def init(api, jwt):
    pass  # expected to use it at /admin page.