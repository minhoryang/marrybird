"""."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from . import db


class ToMarrybird(db.Model):
    __bind_key__ = "tomarrybird"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))
    message = db.Column(db.String(200))


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken', location='headers')
    insert_message = copy(authorization)
    insert_message.add_argument('message', type=str, required=True, location='json')

    @namespace.route('/receive')
    class ToMarrybirdReceiver(Resource):

        @jwt_required()
        @api.doc(parser=insert_message)
        def post(self):
            rec = ToMarrybird()
            rec.username = current_user.username
            rec.message = insert_message.parse_args()['message']
            db.session.add(rec)
            db.session.commit()
            return {'status': 200, 'message': 'received'}, 200