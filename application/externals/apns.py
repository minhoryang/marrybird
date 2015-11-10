__author__ = 'minhoryang'

from contextlib import contextmanager
from os.path import join

from pushjack import APNSClient as APNSClient_

from ..configs import PROJECT_PATH


@contextmanager
def APNSClient():
    apns = APNSClient_(
        certificate=join(
            PROJECT_PATH,
            "application",
            "externals",
            "me_marrybird_app_ios_v1-PRODUCTION.pem"),
        default_error_timeout=1,
        default_batch_size=100,
    )
    yield apns
    apns.close()


class APNSException(Exception): pass


def push(message, token=None, badge=1, sound='default'):
    if token:
        with APNSClient() as apns:
            return {"errors": apns.send(
                token,
                message,
                badge=badge,
                sound=sound,
            ).token_errors}
    else:
        raise APNSException()
