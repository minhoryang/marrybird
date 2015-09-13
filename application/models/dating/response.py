"""All Love-Line starts and ends at here.

1. User comes here for seeing new love-mate. (which was prepared by <Request>-<Compute>)
2. <Response> get the result of latest <Request>.
3. According to <Progress> (which stores the current on-going love-lines), Search 'I love You' and 'You love I'.
4. Using above 'I love You' and 'You love I',

"""
__author__ = 'minhoryang'

from datetime import datetime
from json import loads

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user

from .. import db
from ..record import Record
from ..notice import Notice
from .progress import Progress
from .met import Met_Accepted, Met_Rejected

class Response(db.Model):
    __bind_key__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer)
    username = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now)

    isDone = db.Column(db.Boolean)
    result_json = db.Column(db.String(200))  # TODO : is there db.Column(db.JSON()) ??


def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/')
    class GetResponse(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            """Suggestions, Who I Loved, and Somebody who loved me."""
            username = current_user.username

            latest = Response.query.filter(Response.username == username).order_by(Response.created_at.desc()).first()
            result_json = None
            if latest:
                result_json = loads(latest.result_json)
            else:
                result_json = []

            Success, _Someone, _Mine = Progress.SearchHeLovesSheOrNot(
                Progress.SearchWhoLovesMe(username),
                Progress.SearchMeLovesWho(username)
            )
            for i in [Success, _Someone, _Mine]:
                for j in i:
                    if j in result_json:
                        result_json.remove(j)

            NotYet = []
            Failed = []
            for wanted_lover_username in _Mine:
                hater = Met_Rejected.query.filter(
                    Met_Rejected.A == wanted_lover_username
                ).filter(
                    Met_Rejected.B == username
                ).first()
                if hater:
                    Failed.append(wanted_lover_username)
                else:
                    NotYet.append(wanted_lover_username)

            SomeoneLovesMe = []
            for i in _Someone:
                hater = Met_Rejected.query.filter(
                    Met_Rejected.A == username,
                    Met_Rejected.B == i,
                ).first()
                if not hater:
                    SomeoneLovesMe.append(i)

            return {'status': 200, 'message': {
                'success': {i: Record._get(i) for i in Success},
                'someonelovesme': {i: Record._get(i) for i in SomeoneLovesMe},
                'notyet': {i: Record._get(i) for i in NotYet},
                'failed': {i: Record._get(i) for i in Failed},
                'result': {i: Record._get(i) for i in result_json},
            }}

    @namespace.route('/<string:i>/love/<string:you>')
    class GetLove(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def post(self, i, you):
            """Notify that I LOVE you to backend."""
            #if i != current_user.username:
            #    return {'status': 400, 'message': 'Not You'}, 400  # TODO
            latest = Response.query.filter(Response.username == current_user.username).order_by(Response.created_at.desc()).first()
            response_id = 0
            if latest and you in loads(latest.result_json):  # TODO : It will not work.
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
            """Notify that I HATE You to backend."""
            #if i != current_user.username:
            #    return {'status': 400, 'message': 'Not You'}, 400  # TODO
            db.session.add(Met_Rejected.create(0, i, you))
            db.session.commit()
            return {'status': 200, 'message': 'done'}
