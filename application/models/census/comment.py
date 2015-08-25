"""comments of question."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from .. import db
from ..record import Record


class Comment(db.Model):
    __bind_key__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    question_book_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50))  # TODO : Fast-Cache vs Dont-Caching-it
    comment = db.Column(db.String(200), nullable=False)

    def __setattr__(self, key, value):
        if key == "nickname" and value:
            return  # delegated from below
        elif key == "username" and value:
            super(__class__, self).__setattr__(
                "nickname",
                Record.query.filter(Record.username == value).first().nickname
            )
            super(__class__, self).__setattr__(key, value)
        else:
            super(__class__, self).__setattr__(key, value)


class CommentLike(db.Model):
    __bind_key__ = "commentlike"

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50))

    def __setattr__(self, key, value):
        if key == "nickname" and value:
            return  # delegated from below
        elif key == "username" and value:
            super(__class__, self).__setattr__(
                "nickname",
                Record.query.filter(Record.username == value).first().nickname
            )
            super(__class__, self).__setattr__(key, value)
        else:
            super(__class__, self).__setattr__(key, value)


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_comment = copy(authorization)
    insert_comment.add_argument(
        'comment',
        type=fields.String(),
        required=True,
        help='{"comment": ""}',
        location='json'
    )

    @namespace.route('/')
    class Comments(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            return