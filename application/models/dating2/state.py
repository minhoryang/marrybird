"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum

from .. import db
from .._external_types import (
    EnumType,
)


class StateType(Enum):
    State_02_Abcd = "State_02_Abcd"
    State_04_ABcd = "State_04_ABcd"
    State_06_AbCd = "State_06_AbCd"
    State_08_ABCd = "State_08_ABCd"
    State_09_abcD = "State_09_abcD"
    State_11_aBcD = "State_11_aBcD"
    State_13_abCD = "State_13_abCD"
    State_15_aBCD = "State_15_aBCD"

    @property
    def isA(self):
        return True if self.value[-4] == 'A' else False

    @property
    def isB(self):
        return True if self.value[-3] == 'B' else False

    @property
    def isC(self):
        return True if self.value[-2] == 'C' else False

    @property
    def isD(self):
        return True if self.value[-1] == 'D' else False


class _StateMixIn(object):
    _id = db.Column(db.Integer, primary_key=True)
    _state = db.Column(EnumType(StateType))
    username = db.Column(db.String(50))
    at = db.Column(db.DateTime, default=datetime.now)


class State(_StateMixIn, db.Model):
    __bind_key__ = __tablename__ = "state"

    @staticmethod
    def TransitionTo(current_state, next_state_type):  # TODO : NOT TESTED
        out = OldState()
        out.CopyAndPaste(current_state)
        out.next_state = next_state_type
        db.session.add(out)
        db.session.delete(current_state)
        db.session.commit()


class _StateInheritedMixIn(object):
    def _init(self, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_StateInheritedMixIn, self).__init__(*args, **kwargs)
        self._state = self.__class__.__name__

    def _parent(self):
        return State.query.get(self.id)


# XXX : Generated - State Inherited DB per StateType.
for cls in StateType.__members__.keys():
    globals()[cls] = type(cls, (_StateInheritedMixIn, State), {
        '__init__': _StateInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': State.__bind_key__,
        'id': db.Column(
            db.Integer,
            db.ForeignKey(State.__tablename__ + '._id'),
            primary_key=True
        ),
    })


class _StateCopyMixIn(object):
    copied_at = db.Column(db.DateTime, default=datetime.now)
    next_state = db.Column(EnumType(StateType))

    def CopyAndPaste(self, state):
        for key in _StateMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif '__' not in key:
                self.__setattr__(key, state.__dict__[key])


class OldState(_StateMixIn, _StateCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldstate"


class DeadState(_StateMixIn, _StateCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadstate"

    @staticmethod
    def RestInPeace(now=datetime.now()):  # TODO : NOT TESTED
        target = now - timedelta(days=7)
        for act in OldState.query.filter(
            OldState.at <= target,
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
    pass
