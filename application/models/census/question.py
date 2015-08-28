"""stores the various kinds of the Question."""

__author__ = 'minhoryang'

from json import loads

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ScalarListType, JSONType

from .. import db


class Question(db.Model):
    __bind_key__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(200))

    # XXX : If None -> Essay Answer Needed!
    _expected_answers = db.Column(JSONType(), nullable=True)
    e_a_json = db.Column(db.String(200), nullable=True)
    is_Multiple_Answer_Available = db.Column(db.Boolean, nullable=False)

    _compute_rules = db.Column(JSONType(), nullable=True)
    c_r_json = db.Column(db.String(200), nullable=True)

    @hybrid_property
    def is_Essay_Answer_Needed(self):
        return self._expected_answers == None

    def __setattr__(self, key, value):
        if key == "e_a_json" and value:
            super(__class__, self).__setattr__("_expected_answers", loads(value.replace("'", '"')))
            return
        elif key == "c_r_json" and value:
            super(__class__, self).__setattr__("_compute_rules", loads(value.replace("'", '"')))
            return
        super(__class__, self).__setattr__(key, value)

    def jsonify(self):
        return {
            'question': self.question,
            'is_Essay_Answer_Needed': self.is_Essay_Answer_Needed,
            'is_Multiple_Answer_Available': self.is_Multiple_Answer_Available,
            'expected_answers': self._expected_answers,
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
    compute_type = db.Column(db.String(50), nullable=False)

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

    def jsonify(self, question_included_from=None):
        result = {
            'title': self.title,
            'photo_url': self.photo_url,
            'brief_description': self.brief_description,
            'description': self.description,
        }
        if question_included_from is not None:
            if question_included_from in self.questions:
                question_included_from = self.questions.index(question_included_from) + 1
            result['questions'] = {
                'done': {idx: Question.query.get(idx).jsonify() for idx in self.questions[:question_included_from]},
                'notyet': {idx: Question.query.get(idx).jsonify() for idx in self.questions[question_included_from:]},
            }
        return result


def init(api, jwt):
    pass


def module_init(api, jwt, namespace):
    pass