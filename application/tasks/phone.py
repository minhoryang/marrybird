__author__ = 'minhoryang'

from .. import create_celery


Celery = create_celery()


@Celery.task(bind=True, ignore_result=True)
def PhoneCheckRequest_post(self):
    from .. import db
    from ..externals.slack import push
    from ..models.phone import Phone

    found = Phone.query.filter(
        Phone.celery_id == str(self.request.id)
    ).first()

    # TODO: Need to connect externals/phonenum-check-by-company
    push('휴대폰인증)' + found.phone + ' 로 ' + found.status + ' 를 보내주세요.')

    found.celery_status = 'sent'
    db.session.add(found)
    db.session.commit()

    return '%s - %s' % (found.phone, found.status)
