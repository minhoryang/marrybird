"""handles the log in / register."""
from datetime import datetime
from re import findall

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.restplus import Resource, fields
from flask_jwt import generate_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declared_attr

from . import db

class User(db.Model):
    __bind_key__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    isMale = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __setattr__(self, key, value):
        if key == 'password':
            value = generate_password_hash(value)
        super(User, self).__setattr__(key, value)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class MaleUser(User):
    __bind_key__ = "user"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class FemaleUser(User):
    __bind_key__ = "user"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    flags = kwargs['flags']
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__)

    @namespace.route('/<string:username>')
    @api.doc(responses={200:'Successfully Login', 400:'Bad Request', 404:'Not Found'})
    class Login(Resource):
        wanted = api.parser()
        wanted.add_argument('password', type=str, required=True, help='{"password": ""}', location='json')  # pull out.

        @api.doc(description='hello', parser=wanted)
        def post(self, username):
            """Hello Users."""
            args = self.wanted.parse_args()
            user = User.query.filter(User.username == username).first()
            if user and user.check_password(args['password']):
                return {'status': 200, 'message': generate_token(user)}
            return {'status': 404, 'message': 'Not Found'}, 404

    @namespace.route('/register')
    @api.doc(responses={200:'Successfully Login', 400:'Bad Request', 404: 'Not Found'})
    class Register(Resource):
        register_rules = api.model('Register', {
            'username' : fields.String(required=True, description='username'),
            'password' : fields.String(required=True, description='password'),
            'isMale' : fields.Boolean(required=True)
        })
        wanted = api.parser()
        wanted.add_argument('register', type=register_rules, required=True, help='{"register": {"username": "", "password": "", "isMale": true}}', location='json')

        @api.doc(parser=wanted)
        def put(self):
            """Register User by receiving JSON Post Message."""
            new_user = None
            args = self.wanted.parse_args()
            username = args['register']['username']
            ret = check_username_rule(username)
            if ret:
                return ret
            if args['register']['isMale']:
                new_user = MaleUser(**args['register'])
            else:
                new_user = FemaleUser(**args['register'])
            try:
                db.session.add(new_user)
                from .dating2.state import State_02_A___
                state = State_02_A___()
                state.username = username
                db.session.add(state)
                db.session.commit()
                from ..tasks.dating2.event import WelcomeSuggestion
                if 'celery' in flags:
                    WelcomeSuggestion.delay(username)
                else:
                    WelcomeSuggestion(username)
            except IntegrityError as e:
                db.session.rollback()
                db.session.close()
                return {'status': 400, 'message': 'Existed Account\n'+str(e)}, 400
            return {'status': 200, 'message':'okay'}

    @namespace.route('/checkid/<string:username>')
    @api.doc(responses={200:'Not Found! Okay to go!', 400:'Bad Request', 404:'Exist ID! Failed to go!'})
    class CheckID(Resource):
        def get(self, username):
            """Check If Wanted ID Was Already Existed."""
            ret = check_username_rule(username)
            if ret:
                return ret
            user = User.query.filter(User.username == username).first()
            if user:
                return {'status': 404, 'message': 'Exist ID! Failed to go!'}, 404
            return {'status': 200, 'message': 'Not Found! Okay to go!'}

    def check_username_rule(username):
        if not 5 <= len(username) <= 50:
            return {'status': 400, 'message': 'too short or too long'}, 400
        elif username not in findall("[A-Za-z0-9가-각]+", username):
            return {'status': 400, 'message': 'Can`t Contain that character'}, 400

    @jwt.user_handler
    def load_user(payload):
        return User.query.filter(User.id == payload['user_id']).first()

    @namespace.route('/test/<string:username>')
    class CeleryTest(Resource):
        def get(self, username):
            """is Celery can worked with SQLAlchemy through Flask?"""
            from ..tasks.user import test
            if 'celery' in flags:
                t = test.delay(username)
                return 'called %s ' % (t,)
            else:
                t = test(username)
                return 'called %s ' % (t,)