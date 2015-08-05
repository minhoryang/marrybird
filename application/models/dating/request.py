"""."""
__author__ = 'minhoryang'

from copy import copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property

from .. import db
from .compute import ComputeNow
from .condition import Condition


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))

    # request
    requester = db.Column(db.String(50))
    requested_at = db.Column(db.DateTime, default=datetime.now)
    condition_id = db.Column(db.Integer)

    # response
    response_id = db.Column(db.Integer, nullable=True)
    is_response_ready = column_property(response_id != None)


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class ComputeRequest(Resource):
        @jwt_required()
        @api.doc(parser=authorization)
        def post(self):
            username = current_user.username
            # TODO : Countdown
            # TODO : Notify Unseen Result
            # TODO : Notify Not Reviewed Dating

            latest_condition = Condition.get_latest_condition_by_user(username)
            if not latest_condition:
                return {'status': 404, message: 'No Condition Found'}, 404

            req = Reqeust()
            req.username = username
            req.requester = username
            req.condition_id = last_condition.id
            db.session.add(req)
            db.session.commit()
            ComputeNow(username, last_condition.id)  # TODO : ASYNC, Please!!!!
            return {'status': 200, 'message': 'Request Done.'}

    """
    @namespace.route('/<string:username>')
    class ComputeRequestBySystem(Resource):
        # TODO : LIMIT THIS CALL USED ONLY BY SYSTEM.
        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, username):
            return {'status': 200, 'message': ''}
    """