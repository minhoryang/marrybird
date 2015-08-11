"""handles the user's records."""
from copy import copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.orm import column_property

from . import db
from .user import User

class Record(db.Model):
    __bind_key__ = "record"

    # XXX : Can't Read & Write.
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime)
    is_male = db.Column(db.Boolean)
    username = db.Column(db.String(50), unique=True)

    # XXX : Can't Write
    is_regular_member = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer)

    # XXX : Readable & Writable
    nickname = db.Column(db.String(50), unique=True)
    graduated_school = db.Column(db.String(50))
    graduated_school_major = db.Column(db.String(50))
    job_category = db.Column(db.String(50))
    job = db.Column(db.String(50))
    district = db.Column(db.String(50))
    district_meetable = db.Column(db.String(50))
    birthday = db.Column(db.String(50))  # TODO: format string "2015-08-10"
    height = db.Column(db.String(50))
    religion = db.Column(db.String(50))
    characteristic = db.Column(db.String(50))
    photo_url = db.Column(db.String(50))
    photo_thumbnail_url = db.Column(db.String(50))
    phonenum = db.Column(db.String(20), unique=True)

    regular_company_email = db.Column(db.String(50))
    regular_company_id_photo_url = db.Column(db.String(50))
    regular_company_paper_card_photo_url = db.Column(db.String(50))
    regular_graduated_school_email = db.Column(db.String(50))
    regular_graduated_school_id_photo_url = db.Column(db.String(50))

    def __setattr__(self, key, value):
        # calc
        if key == "birthday" and value:
            super(Record, self).__setattr__("age", Record.parse_age(value))
        # delegated from DB
        if key == "username" and value:
            super(Record, self).__setattr__(
                "is_male",
                User.query.filter(User.username == value).first().isMale
            )
        super(Record, self).__setattr__(key, value)
        super(Record, self).__setattr__('modified_at', datetime.now())

    @staticmethod
    def parse_comma(input):
        for i in input.split(','):
            if i:
                yield i

    @staticmethod
    def parse_age(birthday):
        return 2015 - int(birthday[:4]) + 1

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    CANT_READ_AND_WRITE_AT_CLIENT = ['id', 'created_at', 'modified_at', 'username', 'is_male']
    CANT_WRITE_AT_CLIENT = ['is_regular_member', 'age']
    AVAILABLE = list()

    for i in Record.__dict__.keys():
        if i[0] == '_' or i in CANT_READ_AND_WRITE_AT_CLIENT:
            pass  # XXX : Can't Read at Client.
        else:
            AVAILABLE.append(i)
    AVAILABLE.sort()

    @namespace.route('/')
    class GetKeywordsList(Resource):
        """All Available Keywords List."""
        def get(self):
            return {'status': 200, 'message': AVAILABLE}

    @namespace.route('/<string:username>')
    @api.doc(responses={200:'Successfully Get', 400:'Not You', 401:'Auth Failed', 404:'Not Found'})
    class GetUsersKeywords(Resource):
        # TODO : PULL THIS OUT.
        authorization = api.parser()
        authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, username):
            """Get User's Keyword Contents."""
            if current_user.username != username:
                return {'status': 400, 'message': 'Not You'}, 400

            existed_record = Record.query.filter(Record.username == username).first()
            if existed_record:
                return {'status': 200, 'message': {key : existed_record.__dict__[key] for key in AVAILABLE}}
            else:
                return {'status': 404, 'message': 'Not Found'}, 404

        wanted_changes = copy(authorization)
        wanted_changes.add_argument(
            'records',
            type=api.model('records', {key: fields.String() for key in AVAILABLE}),
            required=True,
            help='{"records": {"nickname": "", ...}}',
            location='json')

        @jwt_required()
        @api.doc(parser=wanted_changes)
        def post(self, username):
            """Set User's Keyword Contents."""
            received_changes = self.wanted_changes.parse_args()['records']

            acceptable_changes = []
            for key in received_changes:
                if received_changes[key]:
                    if key in CANT_WRITE_AT_CLIENT:
                        pass  # XXX : Can't write at Client. (Ignore first)
                    elif key in AVAILABLE:
                        acceptable_changes.append((key, received_changes[key]))

            if current_user.username != username:
                return {'status': 404, 'message': 'Not Found'}, 404

            existed_record = Record.query.filter(Record.username == username).first()
            if not existed_record:
                existed_record = Record(username=username)

            for key, value in acceptable_changes:
                existed_record.__setattr__(key, value)

            try:
                db.session.add(existed_record)
                db.session.commit()
                return {'status': 200, 'message': 'Updated!'}
            except IntegrityError as e:
                return {'status': 400, 'message': 'Existed User&Nick&Phonenum\n'}, 400

    @namespace.route('/checknickname/<string:nickname>')
    @api.doc(responses={200:'Not Found! Okay to go!', 400:'Bad Request', 404:'Exist ID! Failed to go!'})
    class CheckNickname(Resource):
        def get(self, nickname):
            """Check If Wanted ID Was Already Existed."""
            if Record.query.filter(Record.nickname == nickname).first():
                return {'status': 404, 'message': 'Exist Nickname! Failed to go!'}, 404
            return {'status': 200, 'message': 'Not Found! Okay to go!'}
    # TODO : NEED TO PULL THIS RESPONSES and RETURN FORMAT OUT TO utils.restful.returns or responses.
