__author__ = 'minhoryang'

from ... import create_celery

Celery = create_celery()


@Celery.task(ignore_result=True)
def DeliveryToUser(event_id):
    from ... import db
    from ...externals.slack import push
    from ...models.dating2.event import Event
    # TODO
    push('HELLO')
    return 'pushed'


@Celery.task(ignore_result=True)
def SuggestionAll(max=2):
    from ...externals.slack import push
    from ...models import db
    from ...models.dating2.state import State, StateException

    for user in State.query.all():
        try:
            user._state.A()
        except StateException:
            push("%s은 지금 데이트 중이십니다 :)" % (user.username,), "#matching")
        else:
            Suggestion.delay(user.username, max)


@Celery.task(ignore_result=True)
def Suggestion(username, max=2):
    """Event_00_Server_Suggested."""
    from ...externals.slack import push
    from ...models import db
    from ...models.record import Record
    from ...models.dating.met import (
        Met,
        Met_NotResponsed,
    )
    from ...models.dating2.event import Event_00_Server_Suggested

    rec = Record.query.filter(Record.username == username).first()

    # Find her/him!
    result = {}
    for i in Record._parse_comma(rec.district_meetable):
        out = Record.query.filter(
            Record.is_male != rec.is_male,
            Record.district_meetable.contains(i),
            Record.age + 4 >= rec.age,
            Record.age - 4 <= rec.age,
            rec._height + 2 >= Record._height if rec.is_male else Record._height + 2 >= rec._height,
            Record.religion == rec.religion if rec.religion != "무교" else True,
        ).all()
        for j in out:
            result[j] = j.username

    # Not met yet.
    result2 = {}
    for rec, name in result.items():
        out = Met.query.filter(
            Met.A == username,
            Met.B == name
        ).first()
        if not out:
            result2[rec] = name

    # TODO : Regular Member.

    result3 = list(result2.values())[:max]
    if result3:
        for target_name in result3:
            db.session.add(Event_00_Server_Suggested(username, [target_name]))
            db.session.add(Met_NotResponsed.create(0, username, target_name))
        db.session.commit()
        push("%s님에게 %d분 중에서 다음분들을 추천해 드렸습니다 : %s" % (username, len(result2), ' '.join(result3)), "#matching")
        return 'suggested %s' % result3
    else:
        push("@matching : 더이상 %s의 추천 상대를 추천할 수 없습니다." % (username,), "#matching")


def RestInPeace():
    pass
