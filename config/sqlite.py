__author__ = 'minhoryang'

from . import PROJECT_PATH
from application.utils.constant import SQLALCHEMY_DATABASE_URI as sqlalchemy_database_uri  # XXX : Blocking to import as config.


MARRYBIRD_FLAGS = [
    'sqlite',
]

SQLALCHEMY_DATABASE_URI = sqlalchemy_database_uri(
    name='global',
    project_path=PROJECT_PATH,
    category='User',
    flags=MARRYBIRD_FLAGS,
)
