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
