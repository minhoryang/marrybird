__author__ = 'minhoryang'

from . import (
    question,
    reply,
    comment,
)

ENABLE_MODELS = [
    ("Census", question, (
        question.Question,
        question.QuestionBook,
    )),
    ("Census", reply, (
        reply.Reply,
        reply.ReplyBook,
    )),
    ("Census", comment, (
        comment.Comment,
        comment.CommentLike,
    )),
] \
    + []  # XXX : ADD ABOVE