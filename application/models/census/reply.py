"""stores the various kinds of the Reply."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

from .. import db
from .compute import ComputeNow
from .question import QuestionBook, Question


class Reply(db.Model):
    __bind_key__ = "reply"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    question_book_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)

    replied_at = db.Column(db.DateTime, default=datetime.now)
    answer = db.Column(db.String(200), nullable=False)

    def getQuestion(self):
        return Question.query.get(self.question_id)


class ReplyBook(db.Model):
    __bind_key__ = "replybook"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    question_book_id = db.Column(db.Integer, nullable=False)
    max_question_id = db.Column(db.Integer, default=0, nullable=False)

    # compute
    requested_at = db.Column(db.DateTime, nullable=True)
    isDone = column_property(requested_at != None)
    compute_id = db.Column(db.Integer, nullable=True)  # TODO : ASYNC
    computed_at = db.Column(db.DateTime, nullable=True)
    computed_result = db.Column(db.String(200), nullable=True)

    @hybrid_property
    def isResultReady(self):
        return self.compute_id != None and self.computed_at != None and self.computed_result != None

    def _jsonify(self, question_book, is_question_included=False):
        question_included_from = self.max_question_id if is_question_included else None
        result = question_book.jsonify(question_included_from=question_included_from)
        if self.isResultReady:
            result['status'] = 'done'
            result['progress'] = 100
        elif self.isDone:
            result['status'] = 'waiting'
            result['progress'] = 100
        else:
            result['status'] = 'not finished'
            result['progress'] = int(
                (self.max_question_id / question_book.num_of_questions) * 100
            )
        return result

    @staticmethod
    def jsonify(username, question_book, is_question_included=False):
        found_reply_book = __class__.query.filter(
            __class__.username == username,
            __class__.question_book_id == question_book.id,
        ).first()
        if found_reply_book:
            return found_reply_book._jsonify(question_book, is_question_included=is_question_included)
        else:
            question_included_from = 0 if is_question_included else None
            result = question_book.jsonify(question_included_from=question_included_from)
            result['status'] = 'not touched'
            result['progress'] = 0
            return result

    def iter(self):
        for reply in Reply.query.filter(
            Reply.username == self.username,
            Reply.question_book_id == self.question_book_id,
        ).all():
            yield reply


def init(api, jwt):
    pass  # check below - module_init()


def module_init(api, jwt, namespace):
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_answer = copy(authorization)
    insert_answer.add_argument(
        'answer',
        type=str,
        required=True,
        help='{"answer": ""}',
        location='json'
    )

    @namespace.route('/')
    class ReplyBooks(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            """Get List and Status of QuestionBooks"""
            return {'status': 200, 'message': {
                qb.id: ReplyBook.jsonify(current_user.username, qb)
                for qb in QuestionBook.query.all()}
            }, 200

    @namespace.route('/<int:question_book_id>')
    class YourReplyBook(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id):
            """Get (un)Solved Status"""
            found = QuestionBook.query.get(question_book_id)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404

            return {'status': 200, 'message': ReplyBook.jsonify(current_user.username, found, is_question_included=True)}

    @namespace.route('/<int:question_book_id>/result')
    class YourResult(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id):
            """Show results."""
            found = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not found or not found.isDone or not found.isResultReady:
                return {'status': 404, 'message': 'Not Ready'}, 404
            return {'status': 200, 'message': found.computed_result}, 200

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self, question_book_id):
            """Request to calc the result."""
            found = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not found:
                return {'status': 404, 'message': "Not Found"}, 404
            if found.isResultReady:
                return {'status': 400, 'message': 'Already got the result'}, 400
            if found.isDone:
                return {'status': 400, 'message': 'Already Requested'}, 400
            found.requested_at = datetime.now()
            db.session.add(found)
            db.session.commit()
            output = ComputeNow(found.id)
            return {'status': 200, 'message': 'Done.' + str(output)}

    @namespace.route('/<int:question_book_id>/reply/<int:question_id>')
    class YourReply(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id, question_id):
            """Get your reply."""

            found = Reply.query.filter(
                Reply.username == current_user.username,
                Reply.question_book_id == question_book_id,
                Reply.question_id == question_id
            ).first()
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            return {'status': 200, 'message': found.answer}, 200

        @jwt_required()
        @api.doc(parser=insert_answer)
        def post(self, question_book_id, question_id):
            """Set your reply."""
            answer = insert_answer.parse_args()

            check2 = QuestionBook.query.get(question_book_id)
            if not check2:
                return {'status': 404, 'message': 'Not Found'}, 404

            check = Question.query.get(question_id)
            if not check:
                return {'status': 404, 'message': 'Not Found'}, 404
            if check.book_id != question_book_id:
                return {'status': 404, 'message': 'Not Found'}, 404

            register_check = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not register_check:
                register_check = ReplyBook()
                register_check.username = current_user.username
                register_check.question_book_id = question_book_id
                register_check.max_question_id = 0
            if register_check.isDone:
                return {'status': 400, 'message': 'Already Calc Requested'}, 400
            if int(question_id) > register_check.max_question_id:
                register_check.max_question_id = question_id
            db.session.add(register_check)

            found = Reply.query.filter(
                Reply.username == current_user.username,
                Reply.question_book_id == question_book_id,
                Reply.question_id == question_id
            ).first()
            if not found:
                found = Reply()
                found.username = current_user.username
                found.question_book_id = question_book_id
                found.question_id = question_id
            found.answer = answer['answer']
            found.replied_at = datetime.now()
            db.session.add(found)
            db.session.commit()
            return {'status': 200, 'message': "added"}, 200
