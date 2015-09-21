from os.path import abspath, dirname, join

from celery.schedules import crontab
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
    app.config['CELERY_BROKER_URL'] = 'amqp://marrybird:marrybird-localhost@localhost:5672/marrybird'
    app.config['CELERY_BACKEND_URL'] = app.config['CELERY_BROKER_URL']
    app.config['CELERY_IMPORTS'] = [  # TODO : Don't Exposed.
        'application.tasks.user',
        'application.tasks.phone',
        'application.tasks.dating2.action',
        'application.tasks.dating2.event',
        'application.tasks.dating2.state',
    ]
    app.config['CELERY_ACCEPT_CONTENT'] = ['json',]
    app.config['CELERY_TASK_SERIALIZER'] = 'json'
    app.config['CELERY_RESULT_SERIALIZER'] = 'json'
    app.config['CELERY_TIMEZONE'] = 'Asia/Seoul'
    app.config['CELERYBEAT_SCHEDULE'] = {
        'Every-Day-Im-Shuffling': {
            'task': 'application.tasks.dating2.event.SuggestionAll',
            'schedule': crontab(
                # minute='*/2',
                hour='*', minute='*/10'
                # hour='0', minute='30',
            ),
            #'args': (2),
        },
        'Rest-In-Peace--Event':{
            'task': 'application.tasks.dating2.action.RestInPeace',
            'schedule': crontab(hour='2', minute='30'),
        },
        'Rest-In-Peace--Event':{
            'task': 'application.tasks.dating2.event.RestInPeace',
            'schedule': crontab(hour='3', minute='0'),
        },
        'Rest-In-Peace--Event':{
            'task': 'application.tasks.dating2.state.RestInPeace',
            'schedule': crontab(hour='3', minute='30'),
        },
        # 'Knock-Knock-Knock-Penny--Are-You-There' : {
        #     'task': '',
        #     'schedule': crontab(
        #         minute='*/2+1',
        #         # hour='0', minute='0',
        #     ),
        # },
    }
    app.config['CELERY_SEND_TASK_SENT_EVENT'] = True
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10

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

    @app.teardown_request
    def teardown_request(exception):
        db.session.close()

    return app


def create_celery(app=None):
    from celery import Celery

    app = app or create_app(isolated=True)

    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_BACKEND_URL'])
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask

    return celery
