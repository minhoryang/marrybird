from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from application import create_app
from application.models import db

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def debug():
	app.run('0.0.0.0', debug=True, port=5010)

@manager.command
def run():
	from newrelic.agent import initialize
	initialize('config/newrelic.ini')
	app.run("0.0.0.0", debug=True, use_reloader=True, port=5000)

@manager.command
def createdb():
	db.create_all()

if __name__ == "__main__":
	manager.run()
