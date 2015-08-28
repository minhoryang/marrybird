__author__ = 'minhoryang'

from datetime import datetime

from .. import db


def ComputeNow(reply_book_id):
    from .reply import ReplyBook

    found = ReplyBook.query.get(reply_book_id)
    if not found:
        return 'not found'

    found.compute_id = reply_book_id  # TODO : CELERY LIVES HERE!
    found.computed_at = datetime.now()
    found.computed_result = "done"  # TODO : CALC HOW?

    db.session.add(found)
    db.session.commit()
    return found.computed_result
