"""comments of question."""

__author__ = 'minhoryang'

from datetime import datetime

from .. import db
from ..record import Record

# TODO: FEATURE FLAG NEEDED


class Comment(db.Model):
    __bind_key__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    commented_at = db.Column(db.DateTime, default=datetime.now)

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

    def jsonify(self):
        return {
            "nickname": self.nickname,
            "comment": self.comment,
            #"wholikes": [
            #    liker.nickname
            #    for liker in CommentLike.query.filter(
            #        CommentLike.comment_id == self.id,
            #    ).order_by(
            #        CommentLike.id.desc(),
            #    ).all()
            #]
        }


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
    pass  # XXX : handled at <reply>.

def module_init(api, jwt, namespace):
    pass