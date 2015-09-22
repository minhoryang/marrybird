from newrelic.agent import initialize

initialize('config/newrelic.ini', environment='celery')

from application import create_celery
from config import (
    flask as flask_config,
    # sqlite as sqlite_config,
    postgresql as postgresql_config,
    celery as celery_config,
    jwt as jwt_config,
)

app = create_celery(configs=[
    flask_config,
    # sqlite_config,
    postgresql_config,
    celery_config,
    jwt_config,
])
