"""handles the user's records."""
from copy import copy
from datetime import datetime

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from ._base import db
from .user import User

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), unique=True)

    nickname = db.Column(db.String(50), unique=True)
    graduated_school = db.Column(db.String(50))
    graduated_school_major = db.Column(db.String(50))
    job_category = db.Column(db.String(50))
    job = db.Column(db.String(50))
    district = db.Column(db.String(50))
    district_meetable = db.Column(db.String(50))
    birthday = db.Column(db.String(50))  # TODO: format string
    height = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    chararistic = db.Column(db.String(50))
    photo_url = db.Column(db.String(50))

    def __setattr__(self, key, value):
        super(Record, self).__setattr__(key, value)
        super(Record, self).__setattr__('modified_at', datetime.now())

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)
    keywords = list()
    for i in Record.__dict__.keys():
        if i[0] == '_' or i in ['id', 'created_at', 'modified_at', 'username']:
            pass
        else:
            keywords.append(i)
    keywords.sort()

    @namespace.route('/')
    class GetKeywordsList(Resource):
        def get(self):
            return {'status': 200, 'message': keywords}

    @namespace.route('/<string:username>')
    @api.doc(responses={200:'Successfully Get', 400:'Not You', 401:'Auth Failed', 404:'Not Found'})
    class GetUsersKeywords(Resource):
        wanted = api.parser()
        wanted.add_argument('authorization', type=str, required=True, help='Bearer JWT', location='headers')

        @jwt_required()
        @api.doc(parser=wanted)
        def get(self, username):
            """Get User's Keyword Contents."""
            if current_user.username == username:
                rec = Record.query.filter(Record.username == username).first()
                if rec:
                    return {'status': 200, 'message': [{key : rec.__dict__[key]} for key in keywords]}
                else:
                    return {'status': 404, 'message': 'Not Found'}, 404
            else:
                return {'status': 400, 'message': 'Not You'}, 400

        wanted2 = copy(wanted)
        for key in keywords: wanted2.add_argument(key, type=str, location='form')

        @jwt_required()
        @api.doc(parser=wanted2)
        def post(self, username):
            """Set User's Keyword Contents."""
            args = self.wanted.parse_args()
            got = []
            for key in keywords:
                if args[key]:
                    got.append((key, args[key]))
            if current_user.username == username:
                rec = Record.query.filter(Record.username == username).first()
                if not rec:
                    rec = Record(username=username)
                for key, value in got:
                    rec.__dict__[key] = value
                db.session.add(rec)
                db.session.commit()
                return {'status': 200, 'message': 'done'}
            else:
                return {'status': 404, 'message': 'Not Found'}, 404
