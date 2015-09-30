"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum

from flask.ext.restplus import Resource

from .. import db
from .._external_types import (
    EnumType,
)


class StateException(Exception):
    pass


class s(Enum):
    A = 8
    B = 4
    C = 2
    D = 1

    def __int__(self):
        return self.value


class StateCode(Enum):
    State_02_A___ = s.A.value
    State_04_AB__ = s.A.value + s.B.value
    State_06_A_C_ = s.A.value + s.C.value
    State_08_ABC_ = s.A.value + s.B.value + s.C.value
    State_09____D = s.D.value
    State_11__B_D = s.B.value + s.D.value
    State_13___CD = s.C.value + s.D.value
    State_15__BCD = s.D.value + s.C.value + s.D.value

    @property
    def abcd(self):
        return (
            True if self.value >= s.A.value else False,
            True if self.value % s.A.value >= s.B.value else False,
            True if self.value % s.B.value >= s.C.value else False,
            True if self.value % s.C.value >= s.D.value else False,
        )

    @property
    def type(self):
        return StateType[self.name]

    @staticmethod
    def fromType(type):
        return StateCode[type.name]

    def __add__(self, _s):
        return self.value + _s

    def __sub__(self, _s):
        return self.value - _s


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

    def A(self, exception=True):
        if self.abcd[0]:
            return self
        if exception:
            raise StateException('Want A but ~A')

    def a(self, exception=True):
        try:
            self.A()
        except StateException:
            return self
        else:
            if exception:
                raise StateException('Want ~A but A')

    def _A(self, exception=True):
        return self.a(exception=exception)

    def _a(self, exception=True):
        return self.A(exception=exception)

    def B(self, exception=True):
        if self.abcd[1]:
            return self
        if exception:
            raise StateException('Want B but ~B')

    def b(self, exception=True):
        try:
            self.B()
        except StateException:
            return self
        else:
            if exception:
                raise StateException('Want ~B but B')

    def _B(self, exception=True):
        return self.b(exception=exception)

    def _b(self, exception=True):
        return self.B(exception=exception)

    def C(self, exception=True):
        if self.abcd[2]:
            return self
        if exception:
            raise StateException('Want C but ~C')

    def c(self, exception=True):
        try:
            self.C()
        except StateException:
            return self
        else:
            if exception:
                raise StateException('Want ~C but C')

    def _C(self, exception=True):
        return self.c(exception=exception)

    def _c(self, exception=True):
        return self.C(exception=exception)

    def D(self, exception=True):
        if self.abcd[3]:
            return self
        if exception:
            raise StateException('Want D but ~D')

    def d(self, exception=True):
        try:
            self.D()
        except StateException:
            return self
        else:
            if exception:
                raise StateException('Want ~D but D')

    def _D(self, exception=True):
        return self.d(exception=exception)

    def _d(self, exception=True):
        return self.D(exception=exception)


class _StateMixIn(object):
    id__ = db.Column(db.Integer, primary_key=True)
    _state = db.Column(EnumType(StateType))
    username = db.Column(db.String(50))
    at = db.Column(db.DateTime, default=datetime.now)


class State(_StateMixIn, db.Model):
    __bind_key__ = __tablename__ = "state"

    @staticmethod
    def find(username):
        state = State.query.filter(
            State.username == username,
        ).first()
        if not state:
            return None
        return state.link__()

    def link__(self):  # TODO : More Efficient Way such as relationship :(
        target_class = globals()[self._state.value]
        return target_class.query.filter(
            target_class.id__ == self.id__,
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
    namespace = kwargs['namespace']

    if kwargs.get('DEBUG', None):
        @namespace.route('/statetransitiontest/<int:id>')
        class StateTransitionTest(Resource):
            def get(self, id):
                current = State.query.get(id).link__()
                old, next = current.TransitionTo(StateType.State_06_AbCd)
                db.session.add(old)
                db.session.add(next)
                db.session.delete(current)
                db.session.commit()

        @namespace.route('/restinpeacetest')
        class RestInPeaceTest(Resource):
            def get(self):
                DeadState.RestInPeace(timeout=timedelta(minutes=1))


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
