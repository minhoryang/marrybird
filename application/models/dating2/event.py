"""Shall We Dance."""

__author__ = 'minhoryang'

from datetime import datetime, timedelta
from enum import Enum
from json import loads

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property

from .. import db
from .._external_types import (
    EnumType,
    ScalarListType,
)
from ..dating.response import Response
from ..record import Record


class EventType(Enum):
    Event_00_Server_Suggested = "Event_00_Server_Suggested"
    Event_03_AskedOut = "Event_03_AskedOut"
    Event_04_Got_AskedOut = "Event_04_Got_AskedOut"
    Event_05_Got_AskedOut_And_Accept = "Event_05_Got_AskedOut_And_Accept"
    Event_06_Got_AskedOut_And_Reject = "Event_06_Got_AskedOut_And_Reject"
    Event_07_AskedOut_Accepted = "Event_07_AskedOut_Accepted"
    Event_08_EndOfDating = "Event_08_EndOfDating"
    Event_09_EndOfDating_And_Feedback = "Event_09_EndOfDating_And_Feedback"
    Event_99_AskedOut_Rejected = "Event_99_AskedOut_Rejected"


class _EventMixIn(object):
    id__ = db.Column(db.Integer, primary_key=True)
    _type = db.Column(EnumType(EventType))
    username = db.Column(db.String(50))
    _results = db.Column(ScalarListType(separator="\uFF0C"), default=[])
    at = db.Column(db.DateTime, default=datetime.now)


class Event(_EventMixIn, db.Model):
    __bind_key__ = __tablename__ = "event"

    results = db.Column(db.String(200), default="[]")  # TODO : flask-admin.sqla

    def __setattr__(self, key, value):
        if key == 'results' and value:
            self._results = loads(value.replace("'", '"'))
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


class _EventInheritedMixIn(object):
    def _init(self, username, _results, *args, **kwargs):
        """Inject the type when I initialized."""
        super(_EventInheritedMixIn, self).__init__(*args, **kwargs)
        self._type = self.__class__.__name__
        self.username = username
        self._results = _results


class _EventCopyMixIn(object):
    old_at = db.Column(db.DateTime, default=datetime.now)

    def CopyAndPaste(self, event):
        for key in event.__dict__.keys():
            if key == '_sa_instance_state':
                continue
            elif '__' not in key:
                self.__setattr__(key, event.__dict__[key])


class OldEvent(_EventMixIn, _EventCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "oldevent"


class DeadEvent(_EventMixIn, _EventCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadevent"

    dead_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def RestInPeace(now=datetime.now(), timeout=timedelta(days=7)):
        target = now - timeout
        for DB in (Event, OldEvent):
            for evt in DB.query.filter(
                DB.at >= target,
            ).order_by(
                DB.at.asc(),
            ).all():
                out = DeadEvent()
                out.CopyAndPaste(evt)
                db.session.add(out)
                db.session.delete(evt)
        db.session.commit()


def init(**kwargs):
    pass


def module_init(**kwargs):
    api = kwargs['api']
    namespace = kwargs['namespace']
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/events')
    class GetEvents(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self, now=datetime.now()):
            username = current_user.username

            _result_json = {}
            for e in Event_00_Server_Suggested.query.filter(
                Event_00_Server_Suggested.username == username,
            ).all():
                _result_json[e] = e._results

            _Feedbacked = {}
            for e in Event_09_EndOfDating_And_Feedback.query.filter(
                Event_09_EndOfDating_And_Feedback.username == username,
            ).all():
                _Feedbacked[e] = e._results

            _FeedbackNeeded = {}
            for e in Event_08_EndOfDating.query.filter(
                Event_08_EndOfDating.username == username,
            ).all():
                _FeedbackNeeded[e] = e._results

            _Success = {}
            for DB in [Event_05_Got_AskedOut_And_Accept, Event_07_AskedOut_Accepted]:
                for e in DB.query.filter(
                    DB.username == username,
                ).all():
                    _Success[e] = e._results

            _SomeoneLovesMe = {}
            for e in Event_04_Got_AskedOut.query.filter(
                Event_04_Got_AskedOut.username == username,
            ).all():
                _SomeoneLovesMe[e] = e._results

            _NotYet = {}
            for e in Event_03_AskedOut.query.filter(
                Event_03_AskedOut.username == username,
            ).all():
                _NotYet[e] = e._results

            _Failed = {}
            for e in Event_99_AskedOut_Rejected.query.filter(
                Event_99_AskedOut_Rejected.username == username,
            ).all():
                _Failed[e] = e._results

            result_json = {}
            for e, names in _result_json.items():
                for name in names:
                    result_json[name] = Record._get(name)
                    result_json[name]['expired_at'] = 7 - (now - e.at).days

            Feedbacked = {}
            for e, names in _Feedbacked.items():
                for name in names:
                    Feedbacked[name] = Record._get(name)
                    Feedbacked[name]['expired_at'] = 7 - (now - e.at).days

            FeedbackNeeded = {}
            for e, names in _FeedbackNeeded.items():
                for name in names:
                    FeedbackNeeded[name] = Record._get(name)
                    FeedbackNeeded[name]['expired_at'] = 7 - (now - e.at).days

            Success = {}
            for e, names in _Success.items():
                for name in names:
                    Success[name] = Record._get(name)
                    Success[name]['expired_at'] = 7 - (now - e.at).days

            SomeoneLovesMe = {}
            for e, names in _SomeoneLovesMe.items():
                for name in names:
                    SomeoneLovesMe[name] = Record._get(name)
                    SomeoneLovesMe[name]['expired_at'] = 7 - (now - e.at).days

            NotYet = {}
            for e, names in _NotYet.items():
                for name in names:
                    NotYet[name] = Record._get(name)
                    NotYet[name]['expired_at'] = 7 - (now - e.at).days

            Failed = {}
            for e, names in _Failed.items():
                for name in names:
                    Failed[name] = Record._get(name)
                    Failed[name]['expired_at'] = 7 - (now - e.at).days

            return {'status': 200, 'message': {
                'success': Success,
                'someonelovesme': SomeoneLovesMe,
                'notyet': NotYet,
                'failed': Failed,
                'result': result_json,
                'feedbackneeded': FeedbackNeeded,
                'feedbacked': Feedbacked,
            }}

    @namespace.route('/addfortest/<string:i>/<string:you>')
    class AddFeedForTest(Resource):

        @api.doc()
        def get(self, i, you):
            db.session.add(Event_00_Server_Suggested(i, [you]))
            db.session.commit()


# XXX : Generated - Event Inherited DB per EventType.
for cls in EventType.__members__.keys():
    globals()[cls] = type(cls, (_EventInheritedMixIn, Event), {
        '__init__': _EventInheritedMixIn._init,
        '__tablename__': cls.lower(),  # divide the table
        '__bind_key__': Event.__bind_key__,
        'id__': db.Column(
            db.Integer,
            db.ForeignKey(Event.__tablename__ + '.id__'),
            primary_key=True
        ),
        '__link': db.relationship(Event, uselist=False),
    })
