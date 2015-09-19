"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum
from json import loads

from sqlalchemy.ext.hybrid import hybrid_property

from .. import db
from .._external_types import (
    EnumType,
    JSONType,  # TODO : Manual Migration Needed!
)


class ActionType(Enum):
    Action_01_NotResponsed_ByMe = "Action_01_NotResponsed_ByMe"
    Action_02_NotResponsed_ByYou = "Action_02_NotResponsed_ByYou"
    Action_03_AskedOut = "Action_03_AskedOut"
    Action_04_Got_AskedOut = "Action_04_Got_AskedOut"
    Action_05_Got_AskedOut_And_Accept = "Action_05_Got_AskedOut_And_Accept"
    Action_06_Got_AskedOut_And_Reject = "Action_06_Got_AskedOut_And_Reject"
    Action_07_AskedOut_Accepted = "Action_07_AskedOut_Accepted"
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
    def _init(self, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_ActionInheritedMixIn, self).__init__(*args, **kwargs)
        self._type = self.__class__.__name__


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
    pass
