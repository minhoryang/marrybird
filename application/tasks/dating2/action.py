__author__ = 'minhoryang'

from celery import current_app


@current_app.task(ignore_result=True)
def RestInPeace():
    from ...models.dating2.action import DeadAction
    DeadAction.RestInPeace()
