"""."""

__author__ = 'minhoryang'

from enum import Enum
from datetime import datetime

from .. import db
from .._external_types import EnumType, JSONType


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


class ActionMixIn(object):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(EnumType(ActionType), nullable=False)
    fromA = db.Column(db.String(50), nullable=True)
    toB = db.Column(db.String(50), nullable=False)
    at = db.Column(db.DateTime, default=datetime.now)
    json = db.Column(JSONType(), nullable=True)


class Action(ActionMixIn, db.Model):
    __bind_key__ = __tablename__ = "action"


class Action_01_NotResponsed_ByMe(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_01_NotResponsed_ByMe".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_02_NotResponsed_ByYou(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_02_NotResponsed_ByYou".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_03_AskedOut(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_03_AskedOut".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_04_Got_AskedOut(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_04_Got_AskedOut".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_05_Got_AskedOut_And_Accept(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_05_Got_AskedOut_And_Accept".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_06_Got_AskedOut_And_Reject(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_06_Got_AskedOut_And_Reject".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_07_AskedOut_Accepted(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_07_AskedOut_Accepted".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_08_EndOfDating(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_08_EndOfDating".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class Action_09_EndOfDating_And_Feedback(Action):
    __bind_key__ = "action"
    __tablename__ = "Action_09_EndOfDating_And_Feedback".lower()

    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)


class ActionCopyMixIn(object):
    def CopyAndPaste(self, action):
        for key in ActionMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif '__' not in key:
                self.__setattr__(key, action.__dict__[key])


class OldAction(ActionMixIn, ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldaction"


class DeadAction(ActionMixIn, ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadaction"


def init(**kwargs):
    pass


def module_init(**kwargs):
    pass