"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from .. import db
from .progress import Progress

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    isDone = db.Column(db.Boolean)
    result_json = db.Column(db.String(200))  # TODO : is there db.Column(db.JSON()) ??


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class GetResponse(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            username = current_user.username

            latest = Response.query.filter(Response.username == username).order_by(Response.created_at.desc()).first()
            result_json = latest.result_json

            Success, Someone, Mine = Progress.SearchHeLovesSheOrNot(
                Progress.SearchWhoLovesMe(username),
                Progress.SearchMeLovesWho(username)
            )

            # TODO: Check met.
            NotYet = Mine
            Failed = Mine

            return {'status': 200, 'message': {
                'success': Success,
                'someonelovesme': Someone,
                'notyet': NotYet,
                'failed': Failed,
                'result': result_json
            }}

    @namespace.route('/<string:i>/love/<string:you>')
    class GetLove(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def post(self, i, you):
            if i is not current_user.username:
                return {'status': 400, 'message': 'Not You'}, 400  # TODO
            latest = Response.query.filter(Response.username == username).order_by(Response.created_at.desc()).first()
            response_id = 0
            if you in latest.result_json:  # TODO : It will not work.
                response_id = latest.id
            Progress.Love(i, you, response_id)
            # TODO : MET Not Implemented yet.
            return {'status': 200, 'meesage': 'done'}

    @namespace.route('/<string:i>/hate/<string:you>')
    class GetHate(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def post(self, i, you):
            if i is not current_user.username:
                return {'status': 400, 'message': 'Not You'}, 400  # TODO
            latest = Response.query.filter(Response.username == username).order_by(Response.created_at.desc()).first()
            # TODO MET
            return {'status': 200, 'message': 'done'}