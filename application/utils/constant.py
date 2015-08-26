__author__ = 'minhoryang'

SQLALCHEMY_DATABASE_URI = lambda app, name: 'sqlite:///%s/db/%s.db' % (app.config['PROJECT_PATH'], name)
SQLALCHEMY_BINDS_RULES = lambda app, name: app.config['SQLALCHEMY_BINDS'].update({name: SQLALCHEMY_DATABASE_URI(app, name)})