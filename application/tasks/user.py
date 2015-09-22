from celery import current_app


@current_app.task(ignore_result=True)
def test(username):
    from ..models.user import User
    A = User.query.filter(User.username == username).first()
    if A:
        print(A)
        return A.username
    return 'Not found'
