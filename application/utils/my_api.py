__author__ = 'minhoryang'
from flask import url_for

from flask.ext.restplus import Api


class MyApi(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=False)