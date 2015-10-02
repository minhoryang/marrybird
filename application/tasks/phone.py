__author__ = 'minhoryang'

from .. import create_celery

Celery = create_celery()


@Celery.task(bind=True, ignore_result=True)
def PhoneCheckRequest_post(self, phone, status, retries=0, max_retries=10):
    from .. import db
    from ..externals.slack import push
    from ..models.phone import Phone

    found = Phone.query.filter(
        Phone.phone == phone,
        Phone.status == status,
    ).first()
    if not found:
        if retries > max_retries:
            return 'failed - no record'
        if 'celery' in Celery.conf.MARRYBIRD_FLAGS:
            return 'retry - %s' % (PhoneCheckRequest_post.delay(phone, status, retries+1),)
        return PhoneCheckRequest_post(self, phone, status, retries+1)

    # TODO: Need to connect externals/phonenum-check-by-company
    push('휴대폰인증)' + found.phone + ' 로 ' + found.status + ' 를 보내주세요.')

    found.celery_status = 'sent'
    if self.request.id:
        found.celery_id = str(self.request.id)
    db.session.add(found)
    db.session.commit()
    return (phone, status, retries)
