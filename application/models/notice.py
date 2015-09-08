"""Notice per user."""

__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from . import db


class Notice(db.Model):
    __bind_key__ = "notice"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))
    notice = db.Column(db.String(200))
    photo_url = db.Column(db.String(50))

    def jsonify(self):
        return {
            'message': self.notice,
            'photo_url': self.photo_url,
            'datetime': str(self.created_at),
        }

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class GetNotice(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            Notices = Notice.query.filter(Notice.username == current_user.username).all()
            if not Notices:
                Notices = []
            return {'status': 200, 'message': {
                idx: item.jsonify() for idx, item in enumerate(Notices)
            }}, 200
