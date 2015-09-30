"""Apple Push Notification Service."""

__author__ = 'minhoryang'


from copy import deepcopy as copy
from datetime import datetime, timedelta
from enum import Enum

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from . import db
from ._external_types import EnumType


class TokenStatus(Enum):
    LATEST = "LATEST"
    NOT_LATEST = "NOT_LATEST"  # TODO : But Other Device can reachable.
    DONT_KNOW = "DONT_KNOW"
    IGNORE_IT = "IGNORE_IT"


class APNS(db.Model):
    __bind_key__ = "apns"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    lived_at = db.Column(db.DateTime, default=datetime.now)
    lived_days = db.Column(db.Integer, default=0)
    username = db.Column(db.String(50))

    token = db.Column(db.String(200))
    status = db.Column(EnumType(TokenStatus), default=TokenStatus.LATEST)


def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_token = copy(authorization)
    insert_token.add_argument(
        'token',
        type=str,
        required=True,
        help='{"token": "blahblah"}',
        location='json'
    )

    @namespace.route('/update')
    class APNSUpdate(Resource):

        @jwt_required()
        @api.doc(parser=insert_token)
        def post(self):
            """Update User-Device's APNS Token"""
            username = current_user.username
            token = insert_token.parse_args()['token']

            found = APNS.query.filter(
                APNS.username == username,
                APNS.token == token,
                APNS.status == TokenStatus.LATEST,
            ).first()
            if found:
                found.lived_at = datetime.now()
                found.lived_days = (found.lived_at - found.created_at).days
                db.session.add(found)
                db.session.commit()
                return {'status': 200, 'message': 'already registered'}, 200

            # NOT_LATEST all
            found = APNS.query.filter(
                APNS.username == username,
                APNS.status == TokenStatus.LATEST,
            ).all()
            for f in found:
                f.status = TokenStatus.NOT_LATEST
                db.session.add(f)

            new = APNS()
            new.username = username
            new.token = token
            db.session.add(new)

            db.session.commit()
            return {'status': 200, 'message': 'register'}, 200