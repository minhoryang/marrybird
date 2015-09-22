__author__ = 'minhoryang'

from datetime import timedelta


JWT_AUTH_HEADER_PREFIX = 'Bearer'
JWT_AUTH_URL_RULE = None
JWT_EXPIRATION_DELTA = timedelta(hours=1)

MARRYBIRD_FLAGS = [
    'jwt',
]
