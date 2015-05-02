from os.path import abspath, dirname, join

from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.restplus import Api

def create_app():
    app = Flask(__name__)
    app.config['PROJECT_PATH'] = abspath(join(dirname(__file__), '..'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/app.db' % (app.config['PROJECT_PATH'], )
    app.config['secret_key'] = 'developer'  # TODO: need to change.

    from .models import db, user, record
    db.init_app(app)

    admin = Admin(app)
    admin.add_view(ModelView(user.User, db.session))
    admin.add_view(ModelView(record.Record, db.session))

    api = Api(app, version='1.0', title='MarryBird API', description='Hi There!')
    user.init(api)
    record.init(api)

    return app
