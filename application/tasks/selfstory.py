__author__ = 'minhoryang'

from .. import create_celery

Celery = create_celery()


@Celery.task(bind=True, ignore_result=True)
def ILikeYourSelfStory_put(self, target_username, like_nickname):
    from .. import db
    from ..externals.apns import push
    from ..models.apns import APNS, TokenStatus
    from ..models.selfstory import SelfStoryLike

    # get target's apns device_id
    found = APNS.query.filter(
        APNS.username == target_username,
        APNS.status == TokenStatus.LATEST,
    ).first()
    if found:
        device_id = found.token
        device_id = ''.join(device_id.split())
        # send it
        msg = like_nickname + "님이 회원님의 셀프스토리를 좋대요!"
        return push(msg, device_id)
    return {'error': 'device_id notfound for ' + target_username}