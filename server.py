from flask import Flask, request #, jsonify
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.restful import Api, Resource, reqparse
from sqlalchemy.exc import IntegrityError

from db import SESSION, init_db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'helloworld'
admin = Admin(app)
admin.add_view(ModelView(User, SESSION))

@app.route('/')
def index():
    return 'Helloworld'

@app.teardown_request
def shutdown_session(exception=None):
    SESSION.remove()

api = Api(app)

class LogInApi(Resource):
    def get(self, username, password):
        user = User.query.filter(User.name == username).first()
        if user:
            if user.pwd == password:
                return str(user.idx)
        return 'username/password wrong', 401

class RegisterApi(Resource):
    def core(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('pwd', type=str)
        parser.add_argument('gender', type=str)
        args = parser.parse_args()
        if not args['name'] or not args['pwd'] or not args['gender']:
            return 'not sufficient', 404
        if not args['gender'] in ['male', 'female']:
            return 'gender wrong', 404
        gender = False
        if args['gender'] == 'female':
            gender = True
        u = User(args['name'], args['pwd'], True)
        SESSION.add(u)
        try:
            SESSION.commit()
        except IntegrityError:
            return 'already existed username', 400
        return u.idx
    def get(self):
        return self.core()  # XXX : Just for easy debugging.
    def post(self):
        return self.core()


api.add_resource(LogInApi, '/users/<string:username>/<string:password>')
api.add_resource(RegisterApi, '/users')

if __name__ == "__main__":
    init_db()
    app.run('0.0.0.0', port=5000, debug=True)
