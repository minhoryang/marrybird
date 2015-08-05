from datetime import timedelta
from os.path import abspath, dirname, join

from flask import Flask, jsonify
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.restplus import Api
from flask_jwt import JWT

def create_app():
    app = Flask(__name__)
    # TODO: EXTRACT!!!!
    app.config['PROJECT_PATH'] = abspath(join(dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/app.db' % (app.config['PROJECT_PATH'], )
    app.config['SECRET_KEY'] = 'developer'  # TODO: need to change.
    app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
    app.config['JWT_AUTH_URL_RULE'] = None
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(minutes=10)  # TODO: need to change.
    app.config['UPLOAD_FOLDER'] = 'images/'
    app.config['THREADS_PER_PAGE'] = 2
    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'secret'

    from .models import db, user, record, file, phone
    from .models.dating import condition, request, compute, response, progress, met, review
    db.init_app(app)

    admin = Admin(app)
    admin.add_view(ModelView(user.User, db.session))
    admin.add_view(ModelView(user.MaleUser, db.session))
    admin.add_view(ModelView(user.FemaleUser, db.session))

    admin.add_view(ModelView(record.Record, db.session))
    admin.add_view(ModelView(file.File, db.session))
    admin.add_view(ModelView(phone.Phone, db.session))

    admin.add_view(ModelView(condition.Condition, db.session))
    admin.add_view(ModelView(request.Request, db.session))
    #admin.add_view(ModelView(compute.Compute, db.session))
    admin.add_view(ModelView(response.Response, db.session))
    admin.add_view(ModelView(progress.Progress, db.session))
    admin.add_view(ModelView(met.Met, db.session))
    admin.add_view(ModelView(review.Review, db.session))

    class MyJWT(JWT):
        def _error_callback(self, e):
            return jsonify(dict([('status', e.status_code), ('message', e.error + ' - ' + e.description)])), 401, e.headers  # e.status_code

    jwt = MyJWT(app)

    api = Api(app, version='1.1', title='MarryBird API', description='Hi There!')
    user.init(api, jwt)
    record.init(api, jwt)
    file.init(api, jwt)
    phone.init(api, jwt)

    # TODO : is it necessary?
    condition.init(api, jwt)
    request.init(api, jwt)
    compute.init(api, jwt)
    response.init(api, jwt)
    progress.init(api, jwt)
    met.init(api, jwt)
    review.init(api, jwt)


    # TODO : PULL THIS OUT TO utils.jwt.bridger
    if not 'user_callback' in jwt.__dict__:
        @jwt.user_handler
        def load_user(payload):
            return dict()

    return app
