"""number checking (by sending SMS through Slack)."""
__author__ = 'minhoryang'

from random import randrange
from datetime import datetime

from flask.ext.restplus import Resource

from . import db
from .record import Record
from ..externals.slack import push

class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)

    def __setattr__(self, key, value):
        super(Phone, self).__setattr__(key, value)
        super(Phone, self).__setattr__('modified_at', datetime.now())

def init(api, jwt):
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/request/')
    class PhoneCheckRequest(Resource):
        wanted = api.parser()
        wanted.add_argument('phonenum', type=str, required=True, help='{"phonenum": "01062473590"}', location='json')

        @api.doc(parser=wanted)
        def post(self):
            """Request Token and Sending Push to Slack."""
            args = self.wanted.parse_args()
            if not check_phone_number(args['phonenum']):
                return {'status': 400, 'message': 'Wrong Phone Number'}, 400
            # Check Existed User.
            if Record.query.filter(Record.phonenum == args['phonenum']).first():
                return {'status': 400, 'message': 'Already Registered'}
            # Expired Same Numbers
            for i in Phone.query.filter(Phone.phone == args['phonenum']).filter(Phone.status != "expired"):
                i.status = "expired"
                db.session.add(i)
            # TODO: Async-ed Timeout Feature NEEDED!
            db.session.commit()
            # Register
            add = Phone()
            add.phone = args['phonenum']
            add.status = str(randrange(1000, 9999))
            db.session.add(add)
            db.session.commit()
            # XXX: Push to slack(Human Agent)
            # TODO: Need to connect externals/phonenum-check-by-company
            push('휴대폰인증)' + add.phone + ' 로 ' + add.status + ' 를 보내주세요.')
            return {'status': 200, 'message': 'requested'}

    @namespace.route('/validate/<string:phonenum>/<int:token>')
    class PhoneValidate(Resource):
        def get(self, phonenum, token):
            """Validate Token."""
            got = Phone.query.filter(Phone.phone == phonenum).order_by(Phone.created_at.desc()).first()
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