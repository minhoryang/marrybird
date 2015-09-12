from os.path import abspath, dirname, join

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from .models import ENABLE_MODELS, db
from .utils.my_api import MyApi
from .utils.my_jwt import MyJWT
from .utils.constant import *


def create_app():
    app = Flask(__name__)
    # TODO: EXTRACT!!!!
    app.config['PROJECT_PATH'] = abspath(join(dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI(app, 'global')
    app.config['SECRET_KEY'] = 'developer'  # TODO: need to change.
    app.config['UPLOAD_FOLDER'] = 'images/'
    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'secret'
    #app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_BINDS'] = {}
    app.config['PROPAGATE_EXCEPTIONS'] = True

    api = MyApi(app, version='1.1', title='MarryBird API', description='Hi There!')
    jwt = MyJWT(app)
    admin = Admin(app, name="admin")
    db.app = app  # XXX : FIXED DB Context Issue without launching the app.
    db.init_app(app)

    for category, cls, models in ENABLE_MODELS:
        cls.init(api, jwt)
        for model in models:
            SQLALCHEMY_BINDS_RULES(app, model.__bind_key__)
            admin.add_view(ModelView(model, db.session, category=category))

    MyJWT.Bridger(jwt)

    return app, db
