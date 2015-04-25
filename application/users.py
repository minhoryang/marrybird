"""1."""
from flask.ext.restplus import Resource, fields

def init(api):
	namespace = api.namespace(__name__.split('.')[-1], description=__doc__)
	user_rules = api.model('User', {
		'id' : fields.String(required=True, description='cnt-1'),
		'name' : fields.String(required=True, description='nm'),
		'password' : fields.String(required=True, description='pwd')
	})

	@namespace.route('/')
	@api.doc(responses={404: 'User Not Found'}, params={})
	class Users(Resource):
		@api.doc(description='hello')
		@api.marshal_with(user_rules)
		def get(self):
			"""Hello Users."""
			return ''

	@namespace.route('/2')
	class Hello(Resource):
		def get(self):
			return ''
