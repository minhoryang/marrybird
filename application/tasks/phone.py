__author__ = 'minhoryang'

from celery import current_app


@current_app.task(bind=True, ignore_result=True)
def PhoneCheckRequest_post(self, phone, status):
    from .. import db
    from ..externals.slack import push
    from ..models.phone import Phone

    found = Phone.query.filter(
        Phone.phone == phone,
        Phone.status == status,
    ).first()

    # TODO: Need to connect externals/phonenum-check-by-company
    push('휴대폰인증)' + found.phone + ' 로 ' + found.status + ' 를 보내주세요.')

    found.celery_status = 'sent'
    if self.request.id:
        found.celery_id = str(self.request.id)
    db.session.add(found)
    db.session.commit()
    return ret
