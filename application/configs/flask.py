__author__ = 'minhoryang'

from . import PROJECT_PATH


UPLOAD_FOLDER = 'images/'

SECRET_KEY = 'developer'  # TODO: need to change.
CSRF_ENABLED = True
CSRF_SESSION_KEY = 'secret'

# SQLALCHEMY_ECHO = True
SQLALCHEMY_BINDS = {}

PROPAGATE_EXCEPTIONS = True

MARRYBIRD_FLAGS = [
    # 'DEBUG',
]
