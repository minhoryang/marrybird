__author__ = 'minhoryang'

from .. import create_celery

Celery = create_celery()


@Celery.task(bind=True, ignore_result=True)
def PhoneCheckRequest_post(self, phone, status, retries=0, max_retries=10):
    from .. import db
    from ..externals.coolsms_ import push
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

    # XXX: connected externals/phonenum-check-by-company
    out = push(found.status, found.phone)

    # TODO: Recheck "is sent already?" then ignore it.

    found.celery_status = 'sent'
    if self.request.id:
        found.celery_id = str(self.request.id)
    db.session.add(found)
    db.session.commit()
    return (phone, status, retries, out)
