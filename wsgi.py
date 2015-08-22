from newrelic.agent import initialize
initialize('config/newrelic.ini')

from application import create_app
app, _ = create_app()
