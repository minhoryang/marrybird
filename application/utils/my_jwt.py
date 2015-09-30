__author__ = 'minhoryang'

from flask import jsonify
from flask_jwt import JWT


class MyJWT(JWT):
    def __init__(self, app):
        super(__class__, self).__init__(app)
        if 'jwt' not in app.config['MARRYBIRD_FLAGS']:
            raise Exception('No JWT Flag in MARRYBIRD_FLAGS')

    def _error_callback(self, e):
        return jsonify(dict([('status', 401), ('message', e.error + ' - ' + e.description)])), 401, e.headers  # e.status_code

    @staticmethod
    def Bridger(jwt):
        # TODO : Make This Works!
        if not 'user_callback' in jwt.__dict__:
            @jwt.user_handler
            def load_user(payload):
                return dict()