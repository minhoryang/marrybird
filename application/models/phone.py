"""number checking (by sending SMS through Slack)."""
__author__ = 'minhoryang'

from random import randrange
from datetime import datetime

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.exc import IntegrityError

from ._base import db
from ..externals.slack import push

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), unique=True)
    status = db.Column(db.String(10))
    modified_at = db.Column(db.DateTime, default=datetime.now)

    def __setattr__(self, key, value):
        super(Phone, self).__setattr__(key, value)
        super(Phone, self).__setattr__('modified_at', datetime.now())

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/request/')
    class Request(Resource):
        wanted = api.parser()
        wanted.add_argument('phonenum', type=str, required=True, help='{"phonenum": "01062473590"}', location='json')

        @api.doc(parser=wanted)
        def post(self):
            """Request Token and Sending Push to Slack."""
            args = self.wanted.parse_args()
            if not check_phone_number(args['phonenum']):
                return {'status': 400, 'message': 'Wrong Phone Number'}, 400
            add = Phone()
            add.phone = args['phonenum']
            add.status = str(randrange(1000, 9999))
            try:
                db.session.add(add)
                db.session.commit()
            except IntegrityError as e:
                return {'status': 400, 'message': 'Already Requested\n'+str(e)}, 400
            push('휴대폰인증)' + add.phone + ' 로 ' + add.status + ' 를 보내주세요.')
            return {'status': 200, 'message': 'requested'}

    @namespace.route('/validate/<string:phonenum>/<int:token>')
    class Validate(Resource):
        def get(self, phonenum, token):
            """Validate Token."""
            got = Phone.query.filter(Phone.phone == phonenum).first()
            if not got:
                return {'status': 400, 'message': 'Not Found'}, 400
            if got.status != str(token):
                return {'status': 400, 'message': 'Wrong Token'}, 400
            got.status = 'Verified'
            db.session.add(got)
            db.session.commit()
            return {'status': 200, 'message': 'Verified'}

    def check_phone_number(phonenum):
        return True  # TODO

    """
    @namespace.route('/<string:target_username>')
    class Get(Resource):
        wanted = api.parser()
        wanted.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

        @jwt_required()
        @api.doc(parser=wanted)
        def get(self, target_username):
            got = Phone.query.filter(Phone.username == target_username).first()
            if not got:
                return {'status': 400, 'message': 'Not Authorized'}, 400
            if not is_okay_to_get_your_phone_number(current_user, got):
                return {'status': 400, 'message': 'Not Authorized'}, 400
            return {'status': 200, 'message': got.phone}

    def is_okay_to_get_your_phone_number(me, you):
        return True  # TODO
    """