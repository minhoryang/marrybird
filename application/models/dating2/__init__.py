"""Look at .request.Request, It handles all."""
__author__ = 'minhoryang'

from . import (
    action,
    event,
    state,
)


ENABLE_MODELS = [
    ("Dating V2 Action", action, (
        #action.Action,
        action.Action_01_NotResponsed_ByMe,
        action.Action_02_NotResponsed_ByYou,
        action.Action_03_AskedOut,
        action.Action_04_Got_AskedOut,
        action.Action_05_Got_AskedOut_And_Accept,
        action.Action_06_Got_AskedOut_And_Reject,
        action.Action_07_AskedOut_Accepted,
        action.Action_08_EndOfDating,
        action.Action_09_EndOfDating_And_Feedback,
        action.OldAction,
        action.DeadAction,
    )),
    ("Dating V2 State", state, (
        #state.State,
        state.State_02_Abcd,
        state.State_04_ABcd,
        state.State_06_AbCd,
        state.State_08_ABCd,
        state.State_09_abcD,
        state.State_11_aBcD,
        state.State_13_abCD,
        state.State_15_aBCD,
        state.OldState,
        state.DeadState,
    )),
#    ("Dating V2 Event", event, (
#        #event.Event,
#        Event.Event_00_Server_Suggested,  # -> result
#        Event.Event_03_AskedOut,  # -> notyet
#        Event.Event_04_Got_AskedOut,  # -> someonelovesme
#        Event.Event_05_Got_AskedOut_And_Accept,  # -> success
#        Event.Event_06_Got_AskedOut_And_Reject,  # -x
#        Event.Event_07_AskedOut_Accepted,  # -> success
#        Event.Event_99_AskedOut_Rejected,  # -> failed
#        Event.DeadEvent,
#    )),
    (None, type(
        "#MergedNamespace", (), {
            "init": lambda **kwargs: init(**kwargs),
            "module_init": lambda **kwargs: None,
        }
    ), (
    )),
] \
    + []  # XXX : ADD ABOVE


def init(**kwargs):
    merged_namespace = kwargs['api'].namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    for _, target_module, _ in ENABLE_MODELS:
        target_module.module_init(namespace=merged_namespace, **kwargs)
