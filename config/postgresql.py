__author__ = 'minhoryang'

from application.utils.constant import SQLALCHEMY_DATABASE_URI as sqlalchemy_database_uri  # XXX : Blocking to import as config.


MARRYBIRD_FLAGS = [
    'postgresql',
]

SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri(
    name='global',
    flags=MARRYBIRD_FLAGS,
)
SQLALCHEMY_POOL_TIMEOUT = 10
