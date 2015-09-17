"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum
from json import loads

from .. import db
from .._external_types import (
    EnumType,
    ScalarListType,
)


class EventType(Enum):
    Event_00_Server_Suggested = "Event_00_Server_Suggested"
    Event_03_AskedOut = "Event_03_AskedOut"
    Event_04_Got_AskedOut = "Event_04_Got_AskedOut"
    Event_05_Got_AskedOut_And_Accept = "Event_05_Got_AskedOut_And_Accept"
    Event_06_Got_AskedOut_And_Reject = "Event_06_Got_AskedOut_And_Reject"
    Event_07_AskedOut_Accepted = "Event_07_AskedOut_Accepted"
    Event_99_AskedOut_Rejected = "Event_99_AskedOut_Rejected"


class _EventMixIn(object):
    _id = db.Column(db.Integer, primary_key=True)
    _type = db.Column(EnumType(EventType))
    username = db.Column(db.String(50))
    _results = db.Column(ScalarListType(), default=[])
    at = db.Column(db.DateTime, default=datetime.now)


class Event(_EventMixIn, db.Model):
    __bind_key__ = __tablename__ = "event"

    results = db.Column(db.String(200), default="[]")  # TODO : flask-admin.sqla

    def __setattr__(self, key, value):
        if key == 'results' and value:
            self._results = loads(value.replace("'", '"'))
            return
        super(db.Model, self).__setattr__(key, value)


class _EventInheritedMixIn(object):
    def _init(self, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_EventInheritedMixIn, self).__init__(*args, **kwargs)
        self._type = self.__class__.__name__

    def _parent(self):
        return Event.query.get(self.id)


# XXX : Generated - Event Inherited DB per EventType.
for cls in EventType.__members__.keys():
    globals()[cls] = type(cls, (_EventInheritedMixIn, Event), {
        '__init__': _EventInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': Event.__bind_key__,
        'id': db.Column(
            db.Integer,
            db.ForeignKey(Event.__tablename__ + '._id'),
            primary_key=True
        ),
    })


class _EventCopyMixIn(object):
    copied_at = db.Column(db.DateTime, default=datetime.now)

    def CopyAndPaste(self, event):
        for key in _EventMixIn.__dict__.keys():
            if 'id' == key:
                continue
            elif '__' not in key:
                self.__setattr__(key, event.__dict__[key])


class DeadEvent(_EventMixIn, _EventCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadevent"

    @staticmethod
    def RestInPeace(now=datetime.now()):  # TODO : NOT TESTED
        target = now - timedelta(days=7)
        for evt in Event.query.filter(
            Event.at <= target,
        ).order_by(
            Event.at.asc(),
        ).all():
            out = DeadEvent()
            out.CopyAndPaste(evt)
            db.session.add(out)
            db.session.delete(evt)
        db.session.commit()


def init(**kwargs):
    pass


def module_init(**kwargs):
    pass
