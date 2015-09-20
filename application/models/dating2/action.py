"""Shall We Dance."""

__author__ = 'minhoryang'

from copy import deepcopy as copy
from datetime import datetime, timedelta
from enum import Enum
from json import loads
from sys import exc_info

from flask.ext.restplus import Resource, fields
from flask_jwt import jwt_required, current_user
from sqlalchemy.ext.hybrid import hybrid_property
from newrelic.agent import record_exception as newrelic_exception

from .. import db
from .._external_types import (
    EnumType,
    JSONType,  # TODO : Manual Migration Needed!
)
from .event import (
    Event_00_Server_Suggested,
    Event_03_AskedOut,
    Event_04_Got_AskedOut,
    Event_05_Got_AskedOut_And_Accept,
    Event_06_Got_AskedOut_And_Reject,
    Event_07_AskedOut_Accepted,
    Event_08_EndOfDating,
    Event_09_EndOfDating_And_Feedback,
    Event_99_AskedOut_Rejected,
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
    def CopyAndPaste(self, action):
        for key in action.__dict__.keys():
            if key == '_sa_instance_state':
                continue
            elif '__' not in key:
                self.__setattr__(key, action.__dict__[key])


class DeadAction(_ActionMixIn, _ActionCopyMixIn, db.Model):
    __bind_key__ = __tablename__ = "deadaction"

    dead_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def RestInPeace(now=datetime.now(), timeout=timedelta(days=7)):
        target = now - timeout
        for act in Action.query.filter(
            Action.at >= target,
        ).order_by(
            Action.at.asc(),
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
    insert_feedback = copy(authorization)
    insert_feedback.add_argument(
        'feedback',
        type=api.model('feedback', {
            'score': fields.String(),
            'text': fields.String(),
        }),
        required=True,
        help='{"feedback": {"score": "1", "text": "1"}}',
        location='json'
    )

    @namespace.route('/<string:i>/love/<string:you>')
    class Love(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self, i, you):
            # if i != current_user.username:
            #     return {'status': 400, 'message': 'Not You'}, 400  # TODO

            i_state = State.find(i)
            you_state = State.find(you)

            # XXX : Check that 'you' already asked out to 'i'
            found_asked_out = []
            for a in Event_04_Got_AskedOut.query.filter(
                Event_04_Got_AskedOut.username == i,
            ).all():
                found_asked_out.extend(a._results)
            if you not in found_asked_out:
                # XXX : Action 3. Asked out
                for e in Event_00_Server_Suggested.query.filter(
                    Event_00_Server_Suggested.username == i,
                ).all():
                    if you in e._results:
                        return Action3(i_state, you_state, e)
            else:
                # XXX : Action 5. Accept
                return Action5(i_state, you_state, found_asked_out)
            return {'status': 404, 'message': 'not found'}, 404

    @namespace.route('/<string:i>/hate/<string:you>')
    class Hate(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self, i, you):
            # if i != current_user.username:
            #     return {'status': 400, 'message': 'Not You'}, 400  # TODO

            i_state = State.find(i)
            you_state = State.find(you)

            # XXX : Check that 'you' already asked out to 'i'
            found_asked_out = []
            for e in Event_04_Got_AskedOut.query.filter(
                Event_04_Got_AskedOut.username == i,
            ).all():
                found_asked_out.extend(e._results)
            if you in found_asked_out:
                # XXX : Action 4. Hate
                return Action4(i_state, you_state, found_asked_out)
            else:
                return {'status': 404, 'message': 'Not Found'}, 404

    @namespace.route('/<string:i>/goodbye/<string:you>')
    class Goodbye(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def put(self, i, you):
            # if i != current_user.username:
            #     return {'status': 400, 'message': 'Not You'}, 400  # TODO

            i_state = State.find(i)
            you_state = State.find(you)

            # XXX : Check that 'you' and 'i' currently dating.
            found_accepted = Accepts(i)

            if you in found_accepted:
                # XXX : Action 8. EndOfDating (Goodbye)
                return Action8(i_state, you_state, found_accepted)
            else:
                return {'status': 404, 'message': 'Not Found'}, 404

    @namespace.route('/<string:i>/feedback/<string:you>')
    class Feedback(Resource):

        @jwt_required()
        @api.doc(parser=insert_feedback)
        def put(self, i, you):
            # if i != current_user.username:
            #     return {'status': 400, 'message': 'Not You'}, 400  # TODO
            feedback = insert_feedback.parse_args()['feedback']

            found_goodbye = {}
            for e in Event_08_EndOfDating.query.filter(
                Event_08_EndOfDating.username == i
            ).all():
                found_goodbye[e] = e._results

            for goodbye, names in found_goodbye.items():
                if you in names:
                    # XXX : Action 9. EndOfDating_And_Feedback
                    return Action9(i, you, goodbye, feedback)
            return {'status': 404, 'message': 'Not Found'}, 404

    if kwargs.get('DEBUG', None):
        @namespace.route('/feedbacktest', doc=False)
        class FeedbackTest(Resource):

            @api.doc()
            def get(self):
                feedback = Event_09_EndOfDating_And_Feedback.query.get(15)
                for i in feedback._results:
                    print((i, type(i)))  # All Text


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


def Action3(i, you, e):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state.A().b().d()

        old_i_state, new_i_state = i.TransitionTo(
            StateType.fromCode(
                i._state.code + int(s.B)
            )
        )
        if you._state.c(False):
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code + int(s.C)
                )
            )
        else:
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code
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
            old = OldEvent()
            old.CopyAndPaste(e)
            db.session.add(old)
            db.session.delete(e)
        if new_you_state:
            db.session.add(new_you_state)
            db.session.add(old_you_state)
            db.session.delete(you)
        db.session.commit()
    return {'status': 200, 'message': 'asked out'}, 200


def Action4(i, you, found_asked_out):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state.C()
        you._state.B()

        if len(found_asked_out) == 1:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code - int(s.C)
                )
            )
        else:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code
                )
            )
        old_you_state, new_you_state = you.TransitionTo(
            StateType.fromCode(
                you._state.code - int(s.B)
            )
        )
    except StateException:
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Condition'}, 400
    except ValueError:
        newrelic_exception(*exc_info())
        return {'status': 400, 'message': 'Not Available Next State'}, 400
    else:
        db.session.add(Action_06_Got_AskedOut_And_Reject(i.username, you.username))
        db.session.add(Event_06_Got_AskedOut_And_Reject(i.username, [you.username]))
        db.session.add(Event_99_AskedOut_Rejected(you.username, [i.username]))
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
    return {'status': 200, 'message': 'reject'}, 200


def Action5(i, you, found_asked_out):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state.C()
        you._state.B()

        # TODO: all? or not?
        if len(found_asked_out) == 1:
            if i._state.A(False) and i._state.d(False):
                    old_i_state, new_i_state = i.TransitionTo(
                        StateType.fromCode(
                            i._state.code - int(s.A) - int(s.C) + int(s.D)
                        )
                    )
            else:
                old_i_state, new_i_state = i.TransitionTo(
                    StateType.fromCode(
                        i._state.code - int(s.C)
                    )
                )
        else:
            if i._state.A(False) and i._state.d(False):
                old_i_state, new_i_state = i.TransitionTo(
                    StateType.fromCode(
                        i._state.code - int(s.A) + int(s.D)
                    )
                )
            else:
                old_i_state, new_i_state = i.TransitionTo(
                    StateType.fromCode(
                        i._state.code
                    )
                )
        if you._state.A(False) and you._state.d(False):
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code - int(s.A) - int(s.B) + int(s.D)
                )
            )
        else:
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code - int(s.B)
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


def Action8(i, you, found_accepted):
    new_i_state = None
    old_i_state = None
    new_you_state = None
    old_you_state = None
    try:
        i._state.a().D()
        you._state.a().D()

        # TODO: all? or not?
        if len(found_accepted) == 1:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code + int(s.A) - int(s.D)
                )
            )
        else:
            old_i_state, new_i_state = i.TransitionTo(
                StateType.fromCode(
                    i._state.code
                )
            )

        found_accepted_you = Accepts(you.username)

        if len(found_accepted_you) == 1:
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code + int(s.A) - int(s.D)
                )
            )
        else:
            old_you_state, new_you_state = you.TransitionTo(
                StateType.fromCode(
                    you._state.code
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
        db.session.add(Action_08_EndOfDating(i.username, you.username))
        db.session.add(Event_08_EndOfDating(i.username, [you.username]))
        db.session.add(Event_08_EndOfDating(you.username, [i.username]))
        if new_you_state:
            db.session.add(new_you_state)
            db.session.add(old_you_state)
            db.session.delete(you)
            deleted = False
            for DB in [Event_05_Got_AskedOut_And_Accept, Event_07_AskedOut_Accepted]:
                if not deleted:
                    for e in DB.query.filter(
                        DB.username == you.username,
                    ).all():
                        if i.username in e._results:
                            old = OldEvent()
                            old.CopyAndPaste(e)
                            db.session.add(old)
                            db.session.delete(e)
                            deleted = True
                            break
            if not deleted:
                return {'status': 400, 'message': 'Hey You! Did We know each others?'}, 400
        if new_i_state:
            db.session.add(new_i_state)
            db.session.add(old_i_state)
            db.session.delete(i)
            deleted = False
            for DB in [Event_05_Got_AskedOut_And_Accept, Event_07_AskedOut_Accepted]:
                if not deleted:
                    for e in DB.query.filter(
                        DB.username == i.username,
                    ).all():
                        if you.username in e._results:
                            old = OldEvent()
                            old.CopyAndPaste(e)
                            db.session.add(old)
                            db.session.delete(e)
                            deleted = True
                            break
            if not deleted:
                return {'status': 400, 'message': 'Oops! Did We know each others?'}, 400
        db.session.commit()
    return {'status': 200, 'message': 'goodbye'}, 200


def Action9(my_name, your_name, goodbye, feedback):
    db.session.add(Event_09_EndOfDating_And_Feedback(my_name, [your_name, str(feedback)]))
    db.session.delete(goodbye)
    db.session.commit()
    return {'status': 200, 'message': 'feedback'}, 200


def Accepts(username):  # TODO : Func Lamdba :)
    found_accepted = []
    for DB in [Event_05_Got_AskedOut_And_Accept, Event_07_AskedOut_Accepted]:
        for e in DB.query.filter(
            DB.username == username,
        ).all():
            found_accepted.extend(e._results)
    return found_accepted
