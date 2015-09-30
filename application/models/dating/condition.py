"""."""
__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user

from .. import db


class Condition(db.Model):
    __bind_key__ = "condition"

    id = db.Column(db.Integer, primary_key=True)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50))

    index = db.Column(db.Integer)
    value = db.Column(db.String(200))


def init(**kwargs):
    api = kwargs['api']
    jwt = kwargs['jwt']
    namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')
    insert_condition = copy(authorization)
    insert_condition.add_argument('condition', type=api.model('condition', {
        'index': fields.String(),
        'value': fields.String(),
    }), required=True, help='{"condition": {"index": "1"(1~4), "value": "Age++"(200)}}', location='json')

    @namespace.route('/')
    class GetSetYourConditions(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, target=('1','2','3','4')):
            found = Condition.query.filter(
                Condition.username == current_user.username,
            ).order_by(
                Condition.updated_at.desc(),
            ).all()
            result = {key: None for key in target}
            for i in found:
                if not None in result.values():
                    break
                if not result[str(i.index)]:
                    result[str(i.index)] = i.value
            return {'status': 200, 'message': result}, 200

        @jwt_required()
        @api.doc(parser=insert_condition)
        def post(self, target=('1','2','3','4')):
            insert = insert_condition.parse_args()['condition']
            new_one = Condition()
            new_one.username = current_user.username
            if not insert['index'] in target:
                return {'status': 400, 'message': 'wrong index'}, 400
            new_one.index = int(insert['index'])
            new_one.value = insert['value']
            db.session.add(new_one)
            db.session.commit()
            return {'status': 200, 'message': 'added'}, 200