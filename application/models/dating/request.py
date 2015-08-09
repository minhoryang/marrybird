"""."""
__author__ = 'minhoryang'

from copy import copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property

from .. import db
from .compute import ComputeNow
from .response import Response


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))

    # request
    requester = db.Column(db.String(50))
    requested_at = db.Column(db.DateTime, default=datetime.now)

    # response
    response_id = db.Column(db.Integer, nullable=True)
    is_response_ready = column_property(
        db.select(
            [Response.isDone]
        ).where(
            Response.id==response_id
        ).correlate_except(Response)
        #(response_id != None) and (Response.get(response_id).isDone)
    )  # TODO : REPLACE THIS WHEN WE USE CELERY


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


            req = Reqeust()
            req.username = username
            req.requester = username
            db.session.add(req)
            db.session.commit()
            ComputeNow(req.id)  # TODO : ASYNC, Please!!!!
            return {'status': 200, 'message': 'Request Done.'}

        def get(self):  # TEST
            return {'status': 200, 'message':{
                'None' : Request.query.get(1).is_response_ready,
                'False' : Request.query.get(2).is_response_ready,
                'True' : Request.query.get(3).is_response_ready
            }}

    """
    @namespace.route('/<string:username>')
    class ComputeRequestBySystem(Resource):
        # TODO : LIMIT THIS CALL USED ONLY BY SYSTEM.
        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, username):
            return {'status': 200, 'message': ''}
    """