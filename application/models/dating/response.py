"""."""
__author__ = 'minhoryang'

from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from .. import db
from .progress import Progress
from .met import Met_Accepted, Met_Rejected

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
            if latest:
                result_json = latest.result_json
            else:
                result_json = []

            Success, Someone, Mine = Progress.SearchHeLovesSheOrNot(
                Progress.SearchWhoLovesMe(username),
                Progress.SearchMeLovesWho(username)
            )

            NotYet = []
            Failed = []
            for wanted_lover_username in Mine:
                hater = Met_Rejected.query.filter(
                    Met_Rejected.A == wanted_lover_username
                ).filter(
                    Met_Rejected.B == username
                ).first()
                if hater:
                    Failed.append(wanted_lover_username)
                else:
                    NotYet.append(wanted_lover_username)

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
            #if i != current_user.username:
            #    return {'status': 400, 'message': 'Not You'}, 400  # TODO
            latest = Response.query.filter(Response.username == current_user.username).order_by(Response.created_at.desc()).first()
            response_id = 0
            if latest and you in latest.result_json:  # TODO : It will not work.
                response_id = latest.id
            db.session.add(Progress.Love(i, you, response_id))
            db.session.add(Met_Accepted.create(response_id, i, you))
            db.session.commit()
            return {'status': 200, 'meesage': 'done'}

    @namespace.route('/<string:i>/hate/<string:you>')
    class GetHate(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def post(self, i, you):
            #if i != current_user.username:
            #    return {'status': 400, 'message': 'Not You'}, 400  # TODO
            db.session.add(Met_Rejected.create(0, i, you))
            db.session.commit()
            return {'status': 200, 'message': 'done'}