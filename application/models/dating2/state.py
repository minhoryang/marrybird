"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum

from flask.ext.restplus import Resource
from sqlalchemy.ext.hybrid import hybrid_property

from .. import db
from .._external_types import (
    EnumType,
)


class StateCode(Enum):
    State_02_A___ = 8
    State_04_AB__ = 12  # 8 + 4
    State_06_A_C_ = 10  # 8 + 2
    State_08_ABC_ = 14  # 8 + 4 + 2
    State_09____D = 1
    State_11__B_D = 5  # 4 + 1
    State_13___CD = 3  # 2 + 1
    State_15__BCD = 7  # 4 + 2 + 1

    @property
    def abcd(self):
        return (
            True if self.value >= 8 else False,
            True if self.value - 8 >= 4 else False,
            True if self.value - 8 - 4 >= 2 else False,
            True if self.value - 8 - 4 - 2 >= 1 else False,
        )  # TODO : SHAME ON YOU MINHO!

    @property
    def type(self):
        return StateType[self.name]

    @staticmethod
    def fromType(type):
        return StateCode[type.name]


class StateType(Enum):
    State_02_A___ = "State_02_A___"
    State_04_AB__ = "State_04_AB__"
    State_06_A_C_ = "State_06_A_C_"
    State_08_ABC_ = "State_08_ABC_"
    State_09____D = "State_09____D"
    State_11__B_D = "State_11__B_D"
    State_13___CD = "State_13___CD"
    State_15__BCD = "State_15__BCD"

    @property
    def abcd(self):
        return self.code.abcd

    @property
    def code(self):
        return StateCode[self.value]

    @staticmethod
    def fromCode(code):
        found = StateCode(code)
        return StateType(found.name)


class _StateMixIn(object):
    id__ = db.Column(db.Integer, primary_key=True)
    _state = db.Column(EnumType(StateType))
    username = db.Column(db.String(50))
    at = db.Column(db.DateTime, default=datetime.now)


class State(_StateMixIn, db.Model):
    __bind_key__ = __tablename__ = "state"

    @hybrid_property
    def __link(cls):  # TODO : More Efficient Way such as relationship :(
        target_class = globals()[cls._state.value]
        return target_class.query.filter(
            target_class.id__ == cls.id__,
        ).first()

    def __str__(self):
        return 'Linked'  # XXX : Flask-admin


class _StateInheritedMixIn(object):
    def _init(self, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_StateInheritedMixIn, self).__init__(*args, **kwargs)
        self._state = self.__class__.__name__

    def TransitionTo(self, next_state_type):
        old = OldState()
        old.CopyAndPaste(self)
        old.next_state = next_state_type
        next = globals()[next_state_type.value]()
        next._state = next_state_type
        next.username = self.username
        return old, next


# XXX : Generated - State Inherited DB per StateType.
for cls in StateType.__members__.keys():
    globals()[cls] = type(cls, (_StateInheritedMixIn, State), {
        '__init__': _StateInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': State.__bind_key__,
        'id__': db.Column(
            db.Integer,
            db.ForeignKey(State.__tablename__ + '.id__'),
            primary_key=True
        ),
        '__link': db.relationship(State, uselist=False),
    })


class _StateCopyMixIn(object):
    next_state = db.Column(EnumType(StateType))
    old_at = db.Column(db.DateTime, default=datetime.now)

    def CopyAndPaste(self, state):
        for key in state.__dict__.keys():
            if key == '_sa_instance_state':
                continue
            elif '__' not in key:
                self.__setattr__(key, state.__dict__[key])


class OldState(_StateMixIn, _StateCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldstate"


class DeadState(_StateMixIn, _StateCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadstate"

    dead_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def RestInPeace(now=datetime.now(), timeout=timedelta(days=7)):
        target = now - timeout
        for act in OldState.query.filter(
            OldState.at >= target,
        ).order_by(
            OldState.at.asc(),
        ).all():
            out = DeadState()
            out.CopyAndPaste(act)
            db.session.add(out)
            db.session.delete(act)
        db.session.commit()


def init(**kwargs):
    pass


def module_init(**kwargs):
    namespace = kwargs['namespace']

    @namespace.route('/statetransitiontest/<int:id>')
    class StateTransitionTest(Resource):
        def get(self, id):
            current = State.query.get(id).__link
            old, next = current.TransitionTo(StateType.State_06_AbCd)
            db.session.add(old)
            db.session.add(next)
            db.session.delete(current)
            db.session.commit()

    @namespace.route('/restinpeacetest')
    class RestInPeaceTest(Resource):
        def get(self):
            DeadState.RestInPeace(timeout=timedelta(minutes=1))
