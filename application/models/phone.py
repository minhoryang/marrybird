"""number checking (by sending SMS through Slack)."""
__author__ = 'minhoryang'

from random import randrange
from datetime import datetime

from flask.ext.restplus import Resource
from sqlalchemy_utils import UUIDType

from . import db
from .record import Record

class Phone(db.Model):
    __bind_key__ = "phone"

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10))
    status = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    celery_id = db.Column(UUIDType(), nullable=True)  # XXX : db.String(36)
    celery_status = db.Column(db.String(10), nullable=True)

    def __setattr__(self, key, value):
        super(Phone, self).__setattr__(key, value)
        super(Phone, self).__setattr__('modified_at', datetime.now())

def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/request')
    class PhoneCheckRequest(Resource):
        wanted = api.parser()
        wanted.add_argument('phonenum', type=str, required=True, help='{"phonenum": "01062473590"}', location='json')

        @api.doc(parser=wanted)
        def post(self):
            """Request Token and Sending Push to Slack."""
            from ..tasks.phone import PhoneCheckRequest_post

            args = self.wanted.parse_args()
            if not check_phone_number(args['phonenum']):
                return {'status': 400, 'message': 'Wrong Phone Number'}, 400
            # Check Existed User.
            if Record.query.filter(Record.phonenum == args['phonenum']).first():
                return {'status': 400, 'message': 'Already Registered'}
            # Expired Same Numbers
            for i in Phone.query.filter(Phone.phone == args['phonenum']).filter(Phone.status != "expired").all():
                i.status = "expired"
                db.session.add(i)
            # TODO: Async-ed Timeout Feature NEEDED!
            db.session.commit()
            # Register
            add = Phone()
            add.phone = args['phonenum']
            add.status = str(randrange(1000, 9999))
            add.celery_status = 'requested'
            db.session.add(add)
            db.session.commit()
            PhoneCheckRequest_post.delay(add.phone, add.status)
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
