__author__ = 'minhoryang'

from datetime import timedelta

from flask import jsonify
from flask_jwt import JWT


class MyJWT(JWT):
    def __init__(self, app):
        super(__class__, self).__init__(app)
        app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
        app.config['JWT_AUTH_URL_RULE'] = None
        app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)  # TODO: need to change.

    def _error_callback(self, e):
        return jsonify(dict([('status', 401), ('message', e.error + ' - ' + e.description)])), 401, e.headers  # e.status_code

    @staticmethod
    def Bridger(jwt):
        # TODO : Make This Works!
        if not 'user_callback' in jwt.__dict__:
            @jwt.user_handler
            def load_user(payload):
                return dict()