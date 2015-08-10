__author__ = 'minhoryang'

from flask import jsonify
from flask_jwt import JWT


class MyJWT(JWT):
    def _error_callback(self, e):
        return jsonify(dict([('status', e.status_code), ('message', e.error + ' - ' + e.description)])), 401, e.headers  # e.status_code

def MyJWT_Bridger(jwt):
    # TODO : Make This Works!
    if not 'user_callback' in jwt.__dict__:
        @jwt.user_handler
        def load_user(payload):
            return dict()
