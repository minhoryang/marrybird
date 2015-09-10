"""stores the various kinds of the Reply."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime
from json import loads

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property
from sqlalchemy_utils import JSONType

from .. import db
from .compute import ComputeNow
from .question import QuestionBook, Question
from .result import ResultBook


class ReplyMixIn(object):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    question_book_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    question_idx = db.Column(db.Integer, nullable=True)  # forced nullable caused by Migration.

    replied_at = db.Column(db.DateTime, default=datetime.now)
    _answers = db.Column(JSONType(), nullable=True)
    a_json = db.Column(db.String(200), nullable=True)


class Reply(ReplyMixIn, db.Model):
    __bind_key__ =  __tablename__ = "reply"

    def getQuestion(self):
        return Question.query.get(self.question_id)

    def __setattr__(self, key, value):
        if key == "a_json" and value:
            super(__class__, self).__setattr__("_answers", loads(value.replace("'", '"')))
            return
        super(__class__, self).__setattr__(key, value)


class OldReply(ReplyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldreply"

    retries = db.Column(db.Integer)

    def CopyAndPaste(self, replybook):
        for key in ReplyMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif not '__' in key:
                self.__setattr__(key, replybook.__dict__[key])


class ReplyBookMixIn(object):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    question_book_id = db.Column(db.Integer, nullable=False)
    max_question_idx = db.Column(db.Integer, default=0, nullable=False)

    # compute
    requested_at = db.Column(db.DateTime, nullable=True)
    compute_id = db.Column(db.Integer, nullable=True)  # TODO : ASYNC
    computed_at = db.Column(db.DateTime, nullable=True)
    computed_result = db.Column(db.String(200), nullable=True)


class ReplyBook(ReplyBookMixIn, db.Model):
    __bind_key__ = __tablename__ = "replybook"

    @hybrid_property
    def isResultReady(self):
        return self.compute_id != None and self.computed_at != None and self.computed_result != None

    @hybrid_property
    def isDone(self):
        return self.requested_at != None

    def _jsonify(self, question_book, is_question_included=False):
        question_included_from = self.max_question_idx if is_question_included else None
        result = question_book.jsonify(question_included_from=question_included_from)
        if not result:
            return None
        if self.isResultReady:
            result['status'] = 'done'
            result['progress'] = 100
        elif self.isDone:
            result['status'] = 'waiting'
            result['progress'] = 100
        else:
            result['status'] = 'not finished'
            result['progress'] = int(
                (self.max_question_idx / question_book.num_of_questions) * 100
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
            if not result:
                return None
            result['status'] = 'not touched'
            result['progress'] = 0
            return result

    def iter(self):
        for reply in Reply.query.filter(
            Reply.username == self.username,
            Reply.question_book_id == self.question_book_id,
        ).all():
            yield reply


class OldReplyBook(ReplyBookMixIn, db.Model):
    __bind_key__ = __tablename__  = "oldreplybook"

    retries = db.Column(db.Integer)
    retried_at = db.Column(db.DateTime, default=datetime.now)

    def iter(self):
        for oldreply in OldReply.query.filter(
            OldReply.username == self.username,
            OldReply.question_book_id == self.question_book_id,
            OldReply.retries == self.retries,
        ).all():
            yield oldreply

    @staticmethod
    def findMaxRetries(username, question_book_id):
        foundMax = __class__.query.filter(
            __class__.username == username,
            __class__.question_book_id == question_book_id,
        ).order_by(
            __class__.retries.desc(),
        ).first()
        if foundMax:
            return foundMax.retries
        return 0

    def CopyAndPaste(self, replybook):
        for key in ReplyBookMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif not '__' in key:
                self.__setattr__(key, replybook.__dict__[key])


def init(api, jwt):
    pass  # check below - module_init()


def module_init(api, jwt, namespace):
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_answer = copy(authorization)
    insert_answer.add_argument(
        'answer',
        type=list,  # XXX : IT ABSORB ALL "" -> [""], {"": ''} -> [""] (GAE PAN)
        required=True,
        help='{"answer": [""]}',  # "id": __id__}',
        location='json'
    )
    #insert_answer.add_argument(
    #    'id',
    #    type=int,
    #    required=False,
    #    help='if needed'
    #    location='json'
    #)

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
            result = found.computed_result

            description = None
            found = ResultBook.query.filter(
                ResultBook.question_book_id == question_book_id,
                ResultBook.result == result,
            ).first()
            if found:
                description =  found.description
            return {'status': 200, 'message': {'result': result, 'description': description}}, 200

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
            if found.max_question_idx != QuestionBook.query.get(question_book_id).num_of_questions:
                return {'status': 400, 'message': 'Not Finished'}, 400
            found.requested_at = datetime.now()
            db.session.add(found)
            db.session.commit()
            output = ComputeNow(found.id)
            return {'status': 200, 'message': 'Done.' + str(output)}

        @jwt_required()
        @api.doc(parser=authorization)
        def delete(self, question_book_id):
            """Reset your results and all replies."""
            origin_rb = ReplyBook.query.filter(
                ReplyBook.username == current_user.username,
                ReplyBook.question_book_id == question_book_id,
            ).first()
            if not origin_rb:
                return {'status': 404, 'message': "Not Found"}, 404
            if not origin_rb.isResultReady:
                return {'status': 400, 'message': 'Not Yet to get the result'}, 400

            retries = OldReplyBook.findMaxRetries(current_user.username, question_book_id) + 1

            target_rb = OldReplyBook()
            target_rb.CopyAndPaste(origin_rb)
            target_rb.retries = retries
            db.session.add(target_rb)
            db.session.delete(origin_rb)

            for origin_r in origin_rb.iter():
                target_r = OldReply()
                target_r.CopyAndPaste(origin_r)
                target_r.retries = retries
                db.session.add(target_r)
                db.session.delete(origin_r)
            db.session.commit()
            return {'status': 200, 'message': 'reset done'}, 200



    @namespace.route('/<int:question_book_id>/reply/<int:question_idx>')
    class YourReply(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id, question_idx):
            """Get your reply."""
            found = QuestionBook.query.get(question_book_id)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404

            found = Reply.query.filter(
                Reply.username == current_user.username,
                Reply.question_book_id == question_book_id,
                Reply.question_idx == question_idx
            ).first()
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            return {'status': 200, 'message': found._answers}, 200

        @jwt_required()
        @api.doc(parser=insert_answer)
        def post(self, question_book_id, question_idx):
            """Set your reply."""
            answer = insert_answer.parse_args()

            check2 = QuestionBook.query.get(question_book_id)
            if not check2:
                return {'status': 404, 'message': 'Not Found'}, 404
            try:
                question_id = check2.questions[question_idx-1]
            except IndexError:
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
                register_check.max_question_idx = 0
            if register_check.isDone:
                return {'status': 400, 'message': 'Already Calc Requested'}, 400
            db.session.add(register_check)

            found = Reply.query.filter(
                Reply.username == current_user.username,
                Reply.question_book_id == question_book_id,
                Reply.question_idx == question_idx
            ).first()
            if not found:
                found = Reply()
                found.username = current_user.username
                found.question_book_id = question_book_id
                found.question_idx = question_idx
                found.question_id = question_id
                register_check.max_question_idx = max(register_check.max_question_idx, question_idx)
            found._answers = answer['answer']
            found.replied_at = datetime.now()
            db.session.add(found)
            db.session.add(register_check)
            db.session.commit()
            return {'status': 200, 'message': "added"}, 200
