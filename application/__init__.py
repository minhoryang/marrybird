from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from .models import ENABLE_MODELS, db
from .utils.my_api import MyApi
from .utils.my_jwt import MyJWT
from .utils.constant import SQLALCHEMY_BINDS_RULES


def create_app(isolated=False, configs=None):
    app = Flask(__name__)

    if not configs:
        configs = []

    _MARRYBIRD_FLAGS = []
    for c in configs:
        if 'MARRYBIRD_FLAGS' in c.__dict__:
            _MARRYBIRD_FLAGS.extend(c.MARRYBIRD_FLAGS)
        app.config.from_object(c)
    app.config['MARRYBIRD_FLAGS'] = _MARRYBIRD_FLAGS

    db.app = app  # XXX : FIXED DB Context Issue without launching the app.
    db.init_app(app)

    plugins = {}
    if not isolated:
        plugins['admin'] = Admin(app, name="admin")
        plugins['api'] = MyApi(app, version='1.1', title='MarryBird API', description='Hi There!')
        plugins['jwt'] = MyJWT(app)
        plugins['flags'] = app.config['MARRYBIRD_FLAGS']

    for category, cls, models in ENABLE_MODELS:
        if not isolated:
            cls.init(**plugins)  # TODO : NEED TO INVERSE
        for model in models:
            app.config['SQLALCHEMY_BINDS'].update(
                SQLALCHEMY_BINDS_RULES(
                    app.config['PROJECT_PATH'],
                    category,
                    model.__bind_key__,
                    _MARRYBIRD_FLAGS,
                )
            )
            if not isolated:
                plugins['admin'].add_view(ModelView(model, db.session, category=category))

    if not isolated:
        MyJWT.Bridger(plugins['jwt'])

    @app.teardown_request
    def teardown_request(exception):
        db.session.close()

    return app


def create_celery(app=None, configs=None):
    from celery import Celery

    if not configs:
        configs = []

    app = app or create_app(isolated=True, configs=configs)

    celery = Celery(__name__)
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
