"""handles the user's records."""
from datetime import datetime

from flask.ext.restplus import Resource
from flask_jwt import jwt_required
from ._base import db
from .user import User

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), unique=True)

    height = db.Column(db.String(50))
    is_disabled = db.Column(db.String(50))
    is_smoker = db.Column(db.String(50))
    is_drinker = db.Column(db.String(50))
    has_habits = db.Column(db.String(50))
    has_religion = db.Column(db.String(50))
    mbti = db.Column(db.String(10))
    has_car = db.Column(db.String(50))
    has_home = db.Column(db.String(50))
    military = db.Column(db.String(50))
    has_office = db.Column(db.String(50))
    has_office_title = db.Column(db.String(50))
    has_office_salary = db.Column(db.String(50))
    graduated_school = db.Column(db.String(50))
    photo_url = db.Column(db.String(50))

    def __setattr__(self, key, value):
        super(Record, self).__setattr__(key, value)
    #super(Record, self).__setattr__('modified_at', datetime.now)

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)
    keywords = list()
    for i in Record.__dict__.keys():
        if i[0] == '_':
            pass
        elif i in ['id', 'created_at', 'modified_at', 'username']:
            pass
        else:
            keywords.append(i)
    keywords.sort()

    @namespace.route('/')
    class AvailableKeywords(Resource):
        @jwt_required()  # TODO : TEST!!!! and Need to add header info if we want to use it.
        def get(self):
            """Available Keyword List."""
            return {'status':200, 'message': keywords}

    @namespace.route('/<string:username>')
    class GetUsersKeywordsStatus(Resource):
        def get(self, username):
            """Get User's Keywords Status (Inputted or not, then which)."""
            return {'status': 404, 'message': 'User Not Found'}, 404

    @namespace.route('/<string:username>/<string:keyword>')
    class UsersKeywords(Resource):
        def get(self, username, keyword):
            """Get User's Keyword Content."""
            rec = Record.query.filter(Record.username == username).first()
            if rec:
                return rec.__dict__[keyword]
            else:
                return {'status': 404, 'message': 'Not Found'}, 404

        wanted = api.parser()
        wanted.add_argument('value', type=str, required=True, help='{"value": ""}', location='json')

        @api.doc(parser=wanted)
        def post(self, username, keyword):
            """Set User's Keyword Content."""
            self.wanted.parse_args()
            usr = User.query.filter(User.username == username).first()
            if usr:
                rec = Record.query.filter(Record.username == username).first()
                if not rec:
                    rec = Record(username=username)
                rec.__dict__[keyword] = args['value']
                db.session.add(rec)
                db.session.commit()
                return {'status': 200, 'message': 'done'}
            else:
                return {'status': 404, 'message': 'Not Found'}, 404
