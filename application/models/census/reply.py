"""stores the various kinds of the Reply."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

from .. import db
from .question import QuestionBook, Question


class Reply(db.Model):
    __bind_key__ = "reply"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    question_book_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)

    replied_at = db.Column(db.DateTime, default=datetime.now)
    answer = db.Column(db.String(200), nullable=False)


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
    result = db.Column(db.String(200), nullable=True)

    @hybrid_property
    def isResultReady(self):
        return compute_id != None and computed_at != None and result != None

    def getMyReplies(self):
        return Reply.query.filter(
            Reply.username == self.username,
            Reply.question_book_id == self.question_book_id,
        ).order_by(
            Reply.id.desc()
        ).all()

    def getMyLastReply(self):
        if len(self.getMyReplies) > 0:
            return self.getMyReplies[0]
        return None

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
            result = {}
            for qb in QuestionBook.getQuestionBooks():
                result[qb.id] = qb.jsonify()
                found = ReplyBook.query.filter(
                    ReplyBook.username == current_user.username,
                    ReplyBook.question_book_id == qb.id,
                ).first()
                if found:
                    if found.isResultReady:
                        result[qb.id]['result'] = 'done'
                        result[qb.id]['progress'] = 100
                    elif found.isDone:
                        result[qb.id]['result'] = 'waiting'
                        result[qb.id]['progress'] = 100
                    else:
                        result[qb.id]['result'] = 'not finished'
                        result[qb.id]['progress'] = int(
                            found.max_question_id / qb.num_of_questions + 1
                        )
                else:
                    result[qb.id]['result'] = 'not touched'
                    result[qb.id]['progress'] = 0

            return {'status': 200, 'message': result}, 200

    @namespace.route('/<int:question_book_id>')
    class YourReplyBook(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id):
            """Get (un)Solved Status"""
            found = QuestionBook.query.get(question_book_id)
            result = found.jsonify()
            result['questions'] = {
                'done': {},
                'notyet': {},
            }

            MyReplyBook = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not MyReplyBook:
                result['result'] = 'not touched'


            maxDone = MyReplyBook.max_question_id if MyReplyBook else None
            idxOfMaxDone = found.questions.index(maxDone) + 1 if maxDone else 0
            for i in found.questions[:idxOfMaxDone]:
                result['questions']['done'][i] = Question.query.get(i).jsonify()
            for i in found.questions[idxOfMaxDone:]:
                result['questions']['notyet'][i] = Question.query.get(i).jsonify()

            return {'status': 200, 'message': result}

    @namespace.route('/<int:question_book_id>/result')
    class YourResult(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id):
            """Show results and comments."""
            pass  # TODO

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self):
            """Request to calc the result."""
            pass  # TODO

        @jwt_required()
        @api.doc(parser=authorization)
        def head(self):
            """is Ready?"""
            pass  # TODO

    @namespace.route('/<int:question_book_id>/reply/<int:question_id>')
    class YourReply(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id, question_id):
            """Get your reply."""
            check = Question.query.get(question_id)
            if not check:
                return {'status': 400, 'message': 'Target Missed'}, 400
            if check.book_id != question_book_id:
                return {'status': 400, 'message': 'Target Missed'}, 400

            register_check = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not register_check:
                return {'status': 400, 'message': 'Target Missed'}, 400

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

            check = Question.query.get(question_id)
            if not check:
                return {'status': 400, 'message': 'Target Missed'}, 400
            if check.book_id != question_book_id:
                return {'status': 400, 'message': 'Target Missed'}, 400

            register_check = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not register_check:
                register_check = ReplyBook()
                register_check.username = current_user.username
                register_check.question_book_id = question_book_id
                register_check.max_question_id = 0
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
