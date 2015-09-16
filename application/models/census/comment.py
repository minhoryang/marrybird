"""comments of question."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask import current_app
from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy_utils.functions import database_exists

from ...utils.constant import SQLALCHEMY_DATABASE_URI
from .. import db
from ..record import Record
from .reply import ReplyBook


class Comment(db.Model):
    __bind_key__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    commented_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=True)

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
        if CommentLike.isEnabled(current_app):
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
    question_book_id = db.Column(db.Integer, nullable=False)
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
    def isEnabled(_current_app):
        return database_exists(SQLALCHEMY_DATABASE_URI(_current_app, __class__.__bind_key__))


def init(**kwargs):
    pass


def module_init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    namespace = kwargs['namespace']

    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_comment = copy(authorization)
    insert_comment.add_argument(
        'comment',
        type=str,
        required=True,
        help='{"comment": ""}',
        location='json'
    )

    def is_user_finished_this_question_book(username, question_book_id):
        found = ReplyBook.query.filter(
            ReplyBook.username == username,
            ReplyBook.question_book_id == question_book_id,
        ).first()
        if not found:
            return False
        if not found.isResultReady:
            return False
        return True

    @namespace.route('/<int:question_book_id>/comment')
    class NewComment(Resource):

        @jwt_required()
        @api.doc(parser=insert_comment)
        def put(self, question_book_id):
            """Add your comment."""

            if not is_user_finished_this_question_book(current_user.username, question_book_id):
                return {'status': 400, 'message': 'No Yet'}, 400

            insert = insert_comment.parse_args()
            new_one = Comment()
            new_one.question_book_id = question_book_id
            new_one.username = current_user.username
            new_one.content = insert["comment"]
            db.session.add(new_one)
            db.session.commit()
            return {'status': 200, 'message': 'putted'}, 200

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, question_book_id):
            """(Re)Fresh comments."""

            if not is_user_finished_this_question_book(current_user.username, question_book_id):
                return {'status': 400, 'message': 'No Yet'}, 400

            found = Comment.query.filter(
                Comment.question_book_id == question_book_id,
            ).order_by(
                Comment.id.desc(),
            ).all()

            return {'status': 200, 'message': {
                f.id: f.jsonify() for f in found
            }}, 200

    @namespace.route('/<int:question_book_id>/comment/<int:comment_id>')
    class Comments(Resource):

        @jwt_required()
        @api.doc(parser=insert_comment)
        def post(self, question_book_id, comment_id):
            """Modify your comment."""
            insert = insert_comment.parse_args()

            found = Comment.query.get(comment_id)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            if found.question_book_id != question_book_id:
                return {'status': 400, 'message': 'Not This Question Book'}, 400
            if found.username != current_user.username:
                return {'status': 400, 'message': 'Not Yours'}, 400
            found.content = insert['comment']
            found.modified_at = datetime.now()
            db.session.add(found)
            db.session.commit()
            return {'status': 200, 'message': 'modified'}, 200

        @jwt_required()
        @api.doc(parser=authorization)
        def delete(self, question_book_id, comment_id):
            """Delete your comment."""
            found = Comment.query.get(comment_id)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            if found.question_book_id != question_book_id:
                return {'status': 400, 'message': 'Not This Question Book'}, 400
            if found.username != current_user.username:
                return {'status': 400, 'message': 'Not Yours'}, 400
            db.session.delete(found)

            if CommentLike.isEnabled(api.app):
                foundComments = CommentLike.query.filter(
                    CommentLike.question_book_id == question_book_id,
                    CommentLike.comment_id == comment_id,
                ).all()
                db.session.delete(foundComments)

            db.session.commit()
            return {'status': 200, 'message': 'deleted'}, 200

    if CommentLike.isEnabled(api.app):

        @namespace.route('/<int:question_book_id>/comment/<int:comment_id>/like')
        class CommentLikes(Resource):

            @jwt_required()
            @api.doc(parser=authorization)
            def get(self, question_book_id, comment_id):
                """Did I Like it?"""
                found = CommentLike.query.filter(
                    CommentLike.username == current_user.username,
                    CommentLike.question_book_id == question_book_id,
                    CommentLike.comment_id == comment_id,
                ).first()
                if found:
                    return {'status': 200, 'message': 'You Liked it.'}, 200
                else:
                    return {'status': 404, 'message': 'You didn`t like it yet'}, 404

            @jwt_required()
            @api.doc(parser=authorization)
            def put(self, question_book_id, comment_id):
                """Like it."""

                if not is_user_finished_this_question_book(current_user.username, question_book_id):
                    return {'status': 400, 'message': 'No Yet'}, 400

                found = CommentLike.query.filter(
                    CommentLike.username == current_user.username,
                    CommentLike.question_book_id == question_book_id,
                    CommentLike.comment_id == comment_id,
                ).first()
                if found:
                    return {'status': 400, 'message': 'ALREADY Liked it!'}, 400

                like = CommentLike()
                like.username = current_user.username
                like.question_book_id = question_book_id
                like.comment_id = comment_id
                db.session.add(like)
                db.session.commit()
                return {'status': 200, 'message': 'Like it!'}, 200

            @jwt_required()
            @api.doc(parser=authorization)
            def delete(self, question_book_id, comment_id):
                """Oops, Now I Hate it."""
                found = CommentLike.query.filter(
                    CommentLike.username == current_user.username,
                    CommentLike.question_book_id == question_book_id,
                    CommentLike.comment_id == comment_id,
                ).first()
                if not found:
                    return {'status': 400, 'message': 'ALREADY Hated it!'}, 400

                db.session.delete(found)
                db.session.commit()
                return {'status': 200, 'message': 'Now You Hate it!'}, 200
