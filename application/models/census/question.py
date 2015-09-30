"""stores the various kinds of the Question."""

__author__ = 'minhoryang'

from json import loads

from flask.ext.restplus import Resource
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import ScalarListType, JSONType

from .. import db
from ...externals.mbti import MBTI_Question
from ...externals.HEXACO_H import HEXACO_Question as HEXACO_H
from ...externals.HEXACO_E import HEXACO_Question as HEXACO_E
from ...externals.HEXACO_X import HEXACO_Question as HEXACO_X
from ...externals.HEXACO_A import HEXACO_Question as HEXACO_A
from ...externals.HEXACO_C import HEXACO_Question as HEXACO_C
from ...externals.HEXACO_O import HEXACO_Question as HEXACO_O


class Question(db.Model):
    __bind_key__ = "question"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(200))

    # XXX : If None -> Essay Answer Needed!
    _expected_answers = db.Column(JSONType(), nullable=True)
    e_a_json = db.Column(db.String(200), nullable=True)
    expected_answer_count = db.Column(db.Integer, nullable=False)
    is_Essay_Answer_Needed = db.Column(db.Boolean, default=False)

    _compute_rules = db.Column(JSONType(), nullable=True)
    c_r_json = db.Column(db.String(200), nullable=True)

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
            #'__id__': self.id,
            'question': self.question,
            'is_Essay_Answer_Needed': self.is_Essay_Answer_Needed,
            'expected_answer_count': self.expected_answer_count,
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
                'done': {n+1: Question.query.get(idx).jsonify() for n, idx in enumerate(self.questions[:question_included_from])},
                'notyet': {n+1+question_included_from: Question.query.get(idx).jsonify() for n, idx in enumerate(self.questions[question_included_from:])},
            }
        return result


def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/mbti_import/<int:book_idx>')
    class MBTI_Import(Resource):
        def get(self, book_idx):
            for question in MBTI_Question.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_h_import/<int:book_idx>')
    class HEXACO_H_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_H.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_e_import/<int:book_idx>')
    class HEXACO_E_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_E.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_x_import/<int:book_idx>')
    class HEXACO_X_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_X.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_a_import/<int:book_idx>')
    class HEXACO_A_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_A.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_c_import/<int:book_idx>')
    class HEXACO_C_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_C.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200

    @namespace.route('/hexaco_o_import/<int:book_idx>')
    class HEXACO_O_Import(Resource):
        def get(self, book_idx):
            for question in HEXACO_O.loads():
                db.session.add(question.convert(book_id=book_idx))
            db.session.commit()
            return 'Done', 200


def module_init(**kwargs):
    pass