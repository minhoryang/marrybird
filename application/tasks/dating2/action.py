__author__ = 'minhoryang'

from ... import create_celery

Celery = create_celery()


@Celery.task(ignore_result=True)
def RestInPeace():
    from ...models.dating2.action import DeadAction
    DeadAction.RestInPeace()


@Celery.task(ignore_result=True)
def NotResponsedAll():
    from ...models.dating2.event import Event_03_AskedOut

    for event in Event_03_AskedOut.query.all():
        if 'celery' in Celery.conf.MARRYBIRD_FLAGS:
            NotResponsed.delay(event.id__)
        else:
            NotResponsed(event.id__)


@Celery.task(ignore_result=True)
def NotResponsed(event_id):
    from datetime import datetime, timedelta

    from ...externals.slack import push
    from ...models import db
    from ...models.dating2.action import (
        Action_01_NotResponsed_By_Me,
        Action_02_NotResponsed_By_You,
    )
    from ...models.dating2.event import (
        Event_03_AskedOut,
        Event_04_Got_AskedOut,
        Event_06_Got_AskedOut_And_Reject,
        Event_99_AskedOut_Rejected,
    )
    from ...models.dating2.state import (
        State,
        StateType,
        s,
    )
    event = Event_03_AskedOut.query.get(event_id)
    target = datetime.now() - timedelta(minutes=1)

    me = event.username

    my_state = State.find(me)
    my_state._state.B()

    if event.at <= target:
        you = event._results[0]
        your_state = State.find(you)
        your_state._state.C()

        db.session.add(Action_01_NotResponsed_By_Me(you, me))
        db.session.add(Action_02_NotResponsed_By_You(me, you))
        db.session.add(Event_06_Got_AskedOut_And_Reject(you, [me]))
        db.session.add(Event_99_AskedOut_Rejected(me, [you]))

        found_asked_out = Event_04_Got_AskedOut.query.filter(
            Event_04_Got_AskedOut.username == you,
        ).all()
        for your in found_asked_out:
            if me in your._results:
                db.session.delete(your)
                break
        db.session.delete(event)

        new_i_state = None
        old_i_state = None
        new_you_state = None
        old_you_state = None

        old_i_state, new_i_state = my_state.TransitionTo(
            StateType.fromCode(
                my_state._state.code - int(s.B)
            )
        )
        if len(found_asked_out) == 1:
            old_you_state, new_you_state = your_state.TransitionTo(
                StateType.fromCode(
                    your_state._state.code - int(s.C)
                )
            )
        else:
            old_you_state, new_you_state = your_state.TransitionTo(
                StateType.fromCode(
                    your_state._state.code
                )
            )
        if new_i_state:
            db.session.add(new_i_state)
            db.session.add(old_i_state)
            db.session.delete(my_state)
        if new_you_state:
            db.session.add(new_you_state)
            db.session.add(old_you_state)
            db.session.delete(your_state)
        db.session.commit()
        push("%s님의 반응이 없어, %s님과의 매칭을 실패로 처리하였습니다." % (you, me), "#matching")
