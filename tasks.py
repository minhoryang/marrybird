from newrelic.agent import initialize

initialize('config/newrelic.ini', environment='celery')

from application import create_celery

app = create_celery()
