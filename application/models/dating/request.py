"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property

from .. import db
from . import score


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    requested_at = db.Column(db.DateTime, default=datetime.now)

    # response
    response_id = db.Column(db.Integer, nullable=True)
    is_response_sent = column_property(response_id != None)

    # conditions
    conditions = db.Column(db.String(200))  # beauty>>,graduatedschool>3,age<30,...
    # XXX : It will parse later for learning.

def init(api, jwt):
    """
    1. POST /request + Condition Body
      will search score[] and excluded rejected/selected and
    """

    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/')
    class NewRequest(Resource):
        """."""

        @jwt_required()
        @api.doc(responses={200:'Successfully Get', 400:'Not You', 401:'Auth Failed', 404:'Not Found'})
        def post(self):
            return {'status': 200, 'message': ''}
