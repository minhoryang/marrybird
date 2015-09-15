from .. import create_celery

Celery = create_celery()


@Celery.task()
def test(username):
    from ..models.user import User
    A = User.query.filter(User.username == username).first()
    if A:
        print(A)
        return A.username
    return 'Not found'
