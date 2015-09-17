"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum
from json import loads

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
    _id = db.Column(db.Integer, primary_key=True)
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


class _ActionInheritedMixIn(object):
    def _init(self, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_ActionInheritedMixIn, self).__init__(*args, **kwargs)
        self._type = self.__class__.__name__

    def _parent(self):
        return Action.query.get(self.id)


# XXX : Generated - Action Inherited DB per ActionType.
for cls in ActionType.__members__.keys():
    globals()[cls] = type(cls, (_ActionInheritedMixIn, Action), {
        '__init__': _ActionInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': Action.__bind_key__,
        'id': db.Column(
            db.Integer,
            db.ForeignKey(Action.__tablename__ + '._id'),
            primary_key=True
        ),
    })


class _ActionCopyMixIn(object):
    copied_at = db.Column(db.DateTime, default=datetime.now)

    def CopyAndPaste(self, action):
        for key in _ActionMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif '__' not in key:
                self.__setattr__(key, action.__dict__[key])


class OldAction(_ActionMixIn, _ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldaction"


class DeadAction(_ActionMixIn, _ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadaction"

    @staticmethod
    def RestInPeace(now=datetime.now()):  # TODO : NOT TESTED
        target = now - timedelta(days=7)
        for DB in (Action, OldAction):
            for act in DB.query.filter(
                DB.at <= target,
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
