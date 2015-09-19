"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum
from json import loads
from sys import exc_info

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from newrelic.agent import record_exception as newrelic_exception

from .. import db
from .._external_types import (
    EnumType,
    JSONType,  # TODO : Manual Migration Needed!
)
from .event import (
    Event_03_AskedOut,
    Event_04_Got_AskedOut,
    Event_05_Got_AskedOut_And_Accept,
    Event_07_AskedOut_Accepted,
    OldEvent,
)
from .state import (
    State,
    StateException,
    StateType,
    s,
)


class ActionType(Enum):
    Action_03_AskedOut = "Action_03_AskedOut"
    Action_05_Got_AskedOut_And_Accept = "Action_05_Got_AskedOut_And_Accept"
    Action_06_Got_AskedOut_And_Reject = "Action_06_Got_AskedOut_And_Reject"
    Action_08_EndOfDating = "Action_08_EndOfDating"
    Action_09_EndOfDating_And_Feedback = "Action_09_EndOfDating_And_Feedback"


class _ActionMixIn(object):
    id__ = db.Column(db.Integer, primary_key=True)
    _type = db.Column(EnumType(ActionType))
    from_A = db.Column(db.String(50), default="")
    to_B = db.Column(db.String(50), nullable=False)
    at = db.Column(db.DateTime, default=datetime.now)
    _json = db.Column(JSONType(), default=None)


class Action(_ActionMixIn, db.Model):
    __bind_key__ = __tablename__ = "action"

    json = db.Column(db.String(200), default="''")  # TODO : flask-admin.sqla

    def __setattr__(self, key, value):
        if key == 'json' and value:
            self._json = loads(value.replace("'", '"'))
            return
        super(db.Model, self).__setattr__(key, value)

    @hybrid_property
    def __link(cls):  # TODO : More Efficient Way such as relationship :(
        target_class = globals()[cls._type.value]
        return target_class.query.filter(
            target_class.id__ == cls.id__,
        ).first()

    def __str__(self):
        return 'Linked'  # XXX : Flask-admin


class _ActionInheritedMixIn(object):
    def _init(self, from_A, to_B, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_ActionInheritedMixIn, self).__init__(*args, **kwargs)
        self._type = self.__class__.__name__
        self.from_A = from_A
        self.to_B = to_B


class _ActionCopyMixIn(object):
    old_at = db.Column(db.DateTime, default=datetime.now)

    def CopyAndPaste(self, action):
        for key in action.__dict__.keys():
            if key == '_sa_instance_state':
                continue
            elif '__' not in key:
                self.__setattr__(key, action.__dict__[key])


class OldAction(_ActionMixIn, _ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldaction"


class DeadAction(_ActionMixIn, _ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadaction"

    dead_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def RestInPeace(now=datetime.now(), timeout=timedelta(days=7)):
        target = now - timeout
        for DB in (Action, OldAction):
            for act in DB.query.filter(
                DB.at >= target,
            ).order_by(
                DB.at.asc(),
            ).all():
                out = DeadAction()
                out.CopyAndPaste(act)
                db.session.add(out)
                db.session.delete(act)
        db.session.commit()


def init(**kwargs):
    pass


def module_init(**kwargs):
    api = kwargs['api']
    namespace = kwargs['namespace']
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/<string:i>/love/<string:you>')
    class Love(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self, i, you):
            # if i != current_user.username:
            #     return {'status': 400, 'message': 'Not You'}, 400  # TODO

            i_state = State.query.filter(
                State.username == i,
            ).first()
            if not i_state:
                return {'status': 404, 'message': 'Not Found %s' % (i,)}, 404
            i_state = i_state.link__()

            you_state = State.query.filter(
                State.username == you,
            ).first()
            if not you_state:
                return {'status': 404, 'message': 'Not Found %s' % (you,)}, 404
            you_state = you_state.link__()

            # XXX : Check that 'you' already asked out to 'i'
            found_asked_out = []
            for e in Event_04_Got_AskedOut.query.filter(
                Event_04_Got_AskedOut.username == i,
            ).all():
                found_asked_out.extend(e._results)
            if you not in found_asked_out:
                # XXX : Action 3. Asked out
                return Action3(i_state, you_state)
            else:
                # XXX : Action 5. Accept
                return Action5(i_state, you_state, found_asked_out)


# XXX : Generated - Action Inherited DB per ActionType.
for cls in ActionType.__members__.keys():
    globals()[cls] = type(cls, (_ActionInheritedMixIn, Action), {
        '__init__': _ActionInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': Action.__bind_key__,
        'id__': db.Column(
            db.Integer,
            db.ForeignKey(Action.__tablename__ + '.id__'),
            primary_key=True
        ),
        '__link': db.relationship(Action, uselist=False),
    })


def Action3(i, you):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state._a()._B()._D()

        old_i_state, new_i_state = i.TransitionTo(
            StateType.fromCode(
                i._state.code + int(s.B)
            )
        )
        if you._state.c():
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code + int(s.C)
                )
            )
    except StateException:
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Condition'}, 400
    except ValueError:
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Next State'}, 400
    else:
        db.session.add(Action_03_AskedOut(i.username, you.username))
        db.session.add(Event_03_AskedOut(i.username, [you.username]))
        db.session.add(Event_04_Got_AskedOut(you.username, [i.username]))
        if new_i_state:
            db.session.add(new_i_state)
            db.session.add(old_i_state)
            db.session.delete(i)
        if new_you_state:
            db.session.add(new_you_state)
            db.session.add(old_you_state)
            db.session.delete(you)
        db.session.commit()
    return {'status': 200, 'message': 'asked out'}, 200


def Action5(i, you, found_asked_out):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state.C()

        # TODO: all? or not?
        if len(found_asked_out) == 1:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code - int(s.A) - int(s.C) + int(s.D)
                )
            )
        else:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code - int(s.A) + int(s.D)
                )
            )
        old_you_state, new_you_state = you.TransitionTo(
            StateType.fromCode(
                you._state.code - int(s.A) - int(s.B) + int(s.D)
            )
        )
    except StateException as e:
        print(e)
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Condition'}, 400
    except ValueError as e:
        print(e)
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Next State'}, 400
    else:
        db.session.add(Action_05_Got_AskedOut_And_Accept(i.username, you.username))
        db.session.add(Event_05_Got_AskedOut_And_Accept(i.username, [you.username]))
        db.session.add(Event_07_AskedOut_Accepted(you.username, [i.username]))
        if new_you_state:
            db.session.add(new_you_state)
            db.session.add(old_you_state)
            db.session.delete(you)
            for e in Event_03_AskedOut.query.filter(
                Event_03_AskedOut.username == you.username,
            ).all():
                if i.username in e._results:
                    old = OldEvent()
                    old.CopyAndPaste(e)
                    db.session.add(old)
                    db.session.delete(e)
                    break
        if new_i_state:
            db.session.add(new_i_state)
            db.session.add(old_i_state)
            db.session.delete(i)
            for e in Event_04_Got_AskedOut.query.filter(
                Event_04_Got_AskedOut.username == i.username,
            ).all():
                if you.username in e._results:
                    old = OldEvent()
                    old.CopyAndPaste(e)
                    db.session.add(old)
                    db.session.delete(e)
                    break
        db.session.commit()
    return {'status': 200, 'message': 'accept'}, 200
