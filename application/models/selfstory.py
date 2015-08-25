"""User's additional stories with photos."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from . import db
from .record import Record


class SelfStory(db.Model):
    __bind_key__ = "selfstory"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, nullable=True)
    username = db.Column(db.String(50))

    photo_url = db.Column(db.String(50))  # XXX : same length with record.py
    title = db.Column(db.String(50), nullable=True)
    story = db.Column(db.String(200))


class SelfStoryLike(db.Model):
    __bind_key__ = "selfstorylike"

    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    nickname = db.Column(db.String(50))

    def __setattr__(self, key, value):
        if key == "nickname" and value:
            return  # delegated from below
        elif key == "username" and value:
            super(__class__, self).__setattr__(
                "nickname",
                Record.query.filter(Record.username == value).first().nickname
            )
        else:
            super(__class__, self).__setattr__(key, value)


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_selfstory = copy(authorization)
    insert_selfstory.add_argument(
        'self_story',
        type=api.model('self_story', {
            'photo_url': fields.String(),
            'story': fields.String(),
            'title': fields.String()
        }),
        required=True,
        help='{"self_story": {"title": "", "photo_url": "1", "story": "..."}}',
        location='json'
    )

    @namespace.route('/<string:username>')
    class SelfStoriesPerUser(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, username):
            """Get List and Stories."""

            found = SelfStory.query.filter(SelfStory.username == username)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404

            return {'status': 200, 'message': {
                item.id: {
                    'photo_url': item.photo_url,
                    'story': item.story,
                    'title': item.title if item.title else "",
                } for item in found
            }}, 200

        @jwt_required()
        @api.doc(parser=insert_selfstory)
        def put(self, username):
            """Add new."""
            if current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400

            insert = insert_selfstory.parse_args()['self_story']
            new_one = SelfStory()
            new_one.username = username
            new_one.photo_url = insert['photo_url']
            new_one.story = insert['story']
            new_one.title = insert['title']
            db.session.add(new_one)
            db.session.commit()
            return {'status': 200, 'message': 'putted'}, 200

    @namespace.route('/<string:username>/<int:idx>')
    class SelfStories(Resource):

        @jwt_required()
        @api.doc(parser=insert_selfstory)
        def post(self, username, idx):
            """Modify it."""
            if current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400

            found = SelfStory.query.get(idx)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            if found.username != username:
                return {'status': 400, 'message': 'Not Yours'}, 400

            insert = insert_selfstory.parse_args()['self_story']

            found.photo_url = insert['photo_url']
            found.story = insert['story']
            found.title = insert['title']
            found.modified_at = datetime.now()
            db.session.add(found)
            db.session.commit()
            return {'status': 200, 'message': 'modified'}, 200

        @jwt_required()
        @api.doc(parser=authorization)
        def delete(self, username, idx):
            """Delete it."""
            if current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400

            found = SelfStory.query.get(idx)
            if not found:
                return {'status': 404, 'message': 'Not Found'}, 404
            if found.username != username:
                return {'status': 400, 'message': 'Not Yours'}, 400

            db.session.delete(found)
            db.session.commit()
            return {'status': 200, 'message': 'deleted'}, 200
