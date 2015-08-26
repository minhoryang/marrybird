"""comments of question."""

__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy_utils.functions import database_exists

from ...utils.constant import SQLALCHEMY_DATABASE_URI
from .. import db
from ..record import Record


class Comment(db.Model):
    __bind_key__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    commented_at = db.Column(db.DateTime, default=datetime.now)

    question_book_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50))  # TODO : Fast-Cache vs Dont-Caching-it
    photo_url = db.Column(db.String(50))
    content = db.Column(db.String(200), nullable=False)

    def __setattr__(self, key, value):
        if key in [
            "nickname",
            "photo_url",
        ] and value:
            return  # delegated from below
        elif key == "username" and value:
            query = Record.query.filter(Record.username == value).first()
            super(__class__, self).__setattr__(
                "nickname",
                query.nickname
            )
            super(__class__, self).__setattr__(
                "photo_url",
                query.photo_url
            )
        super(__class__, self).__setattr__(key, value)

    def jsonify(self):
        result = {
            "nickname": self.nickname,
            "photo_url": self.photo_url,
            "comment": self.content,
        }
        if CommentLike.isEnabled():
            result["wholikes"] = self.getLikes()
        return result

    def getLikes(self):
        return [
            liker.nickname
            for liker in CommentLike.query.filter(
                CommentLike.comment_id == self.id,
            ).order_by(
                CommentLike.id.desc(),
            ).all()
        ]


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

    @staticmethod
    def isEnabled(current_app):
        return database_exists(SQLALCHEMY_DATABASE_URI(current_app, __class__.__bind_key__))


def init(api, jwt):
    pass

def module_init(api, jwt, namespace):
    @namespace.route('/<int:question_book_id>/comment/<int:comment_id>')
    class Comments(Resource):
        def put(self):
            """Add new comment."""
            pass
        def post(self):
            """Modify your comment."""
            pass
        def delete(self):
            """Delete your comment."""
            pass

    if CommentLike.isEnabled(api.app):
        @namespace.route('/<int:question_book_id>/comment/<int:comment_id>/like')
        class CommentLikes(Resource):
            def head(self):
                """Did I Like it?"""
                pass
            def put(self):
                """Like it."""
                pass
            def delete(self):
                """Oops, Now I Hate it."""
                pass