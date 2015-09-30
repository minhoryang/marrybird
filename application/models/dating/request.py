"""Handle User's Matching Process <Request>.

1. <Request> will fire at 12:00am by me(in person) manually
2. Then It register the request log at <Request> DB
3. Then It <Compute.ComputeNow> will make a result.

GOTO: Compute
"""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property

from .. import db
from .compute import ComputeNow
from .response import Response


class Request(db.Model):
    __bind_key__ = "request"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))

    # request
    requester = db.Column(db.String(50))
    requested_at = db.Column(db.DateTime, default=datetime.now)

    # response
    response_id = db.Column(db.Integer, nullable=True)
    #is_response_ready = column_property(
    #    db.select(
    #        [Response.isDone]
    #    ).where(
    #        Response.id==response_id
    #    ).correlate_except(Response)
    #)
    # TODO : REPLACE THIS WHEN WE USE CELERY


def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']

    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class ComputeRequest(Resource):
        # TODO : Countdown
        # TODO : Notify Unseen Result
        # TODO : Notify Not Reviewed Dating

        @jwt_required()
        @api.doc(parser=authorization)
        def post(self):
            """Request the matching suggesstion process to backend. (could be Celery.)"""
            username = current_user.username

            req = Request()
            req.username = username
            req.requester = username
            db.session.add(req)
            db.session.commit()
            output = ComputeNow(req.id)
            db.session.close()  # XXX : After db.session.close() you can't use the variables from DB.
            return {'status': 200, 'message': 'Done.' + str(output)}
    @namespace.route('/<string:username>')
    class ComputeRequestBySystem(Resource):
        # TODO : LIMIT THIS CALL USED ONLY BY SYSTEM.
        def get(self, username):
            req = Request()
            req.username = username
            req.requester = username
            db.session.add(req)
            db.session.commit()
            output = ComputeNow(req.id)
	    db.session.close()  # XXX : After db.session.close() you can't use the variables from DB.
            return {'status': 200, 'message': 'Done.' + str(output)}
