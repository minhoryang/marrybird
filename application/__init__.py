from os.path import abspath, dirname, join

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from .models import ENABLE_MODELS, db
from .utils.my_api import MyApi
from .utils.my_jwt import MyJWT
from .utils.constant import *


def create_app(isolated=False):
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

    db.app = app  # XXX : FIXED DB Context Issue without launching the app.
    db.init_app(app)

    plugins = {}
    if not isolated:
        plugins['admin'] = Admin(app, name="admin")
        plugins['api'] = MyApi(app, version='1.1', title='MarryBird API', description='Hi There!')
        plugins['jwt'] = MyJWT(app)

    for category, cls, models in ENABLE_MODELS:
        if not isolated:
            cls.init(**plugins)  # TODO : NEED TO INVERSE
        for model in models:
            SQLALCHEMY_BINDS_RULES(app, model.__bind_key__)
            if not isolated:
                plugins['admin'].add_view(ModelView(model, db.session, category=category))

    if not isolated:
        MyJWT.Bridger(plugins['jwt'])

    return app


def create_celery(app=None):
    from celery import Celery

    app = app or create_app(isolated=True)

    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery