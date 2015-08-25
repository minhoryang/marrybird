"""stores the various kinds of the Reply."""

__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property

from .. import db


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
            Reply.replied_at.desc()
        ).all()



def init(api, jwt):
    namespace = api.namespace('census')  # TODO: , description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class ReplyBooks(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            """Get List of QuestionBooks-Questions, isDone?-ResultIt."""
            # list of question books
            #    how many people did this
            #    how much percent did I reply?
            #    list?
            return

    @namespace.route('/')
    class Replys(Resource):

        def get(self):
            pass