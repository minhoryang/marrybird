"""
__author__ = 'minhoryang'

from .. import create_celery

Celery = create_celery()


@Celery.task(bind=True, ignore_result=True)
def _post(self):
    from .. import db
    from ..externals.apns import push

    return ()
"""