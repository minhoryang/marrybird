from flask import Flask, Blueprint, redirect
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from .models import ENABLE_MODELS, db
from .utils.my_api import MyApi
from .utils.my_jwt import MyJWT
from .utils.constant import SQLALCHEMY_BINDS_RULES
from .configs import (
    flask as flask_config,
    sqlite as sqlite_config,
    postgresql as postgresql_config,
    celery as celery_config,
    jwt as jwt_config,
)


VERSION = "v1.0"


def create_app(isolated=False):
    app = Flask(__name__)
    versioning = Blueprint('marrybird', __name__)

    _MARRYBIRD_FLAGS = []
    for c in [
        flask_config,
        # sqlite_config,
        postgresql_config,
        celery_config,
        jwt_config,
    ]:
        if 'MARRYBIRD_FLAGS' in c.__dict__:
            _MARRYBIRD_FLAGS.extend(c.MARRYBIRD_FLAGS)
        app.config.from_object(c)
    app.config['MARRYBIRD_FLAGS'] = _MARRYBIRD_FLAGS

    db.app = app  # XXX : FIXED DB Context Issue without launching the app.
    db.init_app(app)

    plugins = {}
    if not isolated:
        plugins['admin'] = Admin(app, name="admin")
        plugins['api'] = MyApi(versioning, version=VERSION, title='MarryBird API', description='Hi There!')
        plugins['configs'] = app.config
        plugins['flags'] = plugins['configs']['MARRYBIRD_FLAGS']
        plugins['jwt'] = MyJWT(app)
        # plugins['DEBUG'] = True

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
        app.register_blueprint(
            versioning,
            url_prefix='/%s' % (VERSION,)
        )
        MyJWT.Bridger(plugins['jwt'])

    @app.route('/')
    def index():
        if not isolated:
            return redirect(VERSION)
        else:
            return '%s isolated' % (VERSION,)  # XXX : Will not show.

    @app.teardown_request
    def teardown_request(exception):
        db.session.close()

    return app


def create_celery(app=None):
    from celery import Celery

    app = app or create_app(isolated=True)

    celery = Celery(__name__, broker=app.config.get('CELERY_BROKER_URL', None), backend=app.config.get('CELERY_BACKEND_URL', None))
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
