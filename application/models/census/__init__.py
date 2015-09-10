"""."""
__author__ = 'minhoryang'

from . import (
    question,
    reply,
    comment,
    result,
)


ENABLE_MODELS = [
    ("Census", question, (
        question.Question,
        question.QuestionBook,
    )),
    ("Census", reply, (
        reply.Reply,
        reply.ReplyBook,
        reply.OldReply,
        reply.OldReplyBook,
    )),
    ("Census", comment, (
        comment.Comment,
        # comment.CommentLike,
    )),
    ("Census", result, (
        result.ResultBook,
    )),
    (None, type(
        "#MergedNamespace", (), {
            "init": lambda *args, **kwargs: init(*args, **kwargs),
            "module_init": lambda *args, **kwargs: None,
        }
    ), (
    )),
] \
    + []  # XXX : ADD ABOVE


def init(api, jwt):
    merged_namespace = api.namespace(__name__.split('.')[-1], description=__doc__.split('.')[0])
    for _, target_module, _ in ENABLE_MODELS:
        target_module.module_init(api, jwt, merged_namespace)
