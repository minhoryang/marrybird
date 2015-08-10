from os.path import abspath, dirname, join

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.restplus import Api

from .models import ENABLE_MODELS, db
from .utils.my_jwt import MyJWT


def create_app():
    app = Flask(__name__)
    # TODO: EXTRACT!!!!
    app.config['PROJECT_PATH'] = abspath(join(dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/app.db' % (app.config['PROJECT_PATH'], )
    app.config['SECRET_KEY'] = 'developer'  # TODO: need to change.
    app.config['UPLOAD_FOLDER'] = 'images/'
    app.config['THREADS_PER_PAGE'] = 2
    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'secret'

    api = Api(app, version='1.1', title='MarryBird API', description='Hi There!')
    jwt = MyJWT(app)
    admin = Admin(app, name="admin")
    db.init_app(app)

    for category, cls, models in ENABLE_MODELS:
        cls.init(api, jwt)
        for model in models:
            admin.add_view(ModelView(model, db.session, category=category))

    MyJWT.Bridger(jwt)

    return app
