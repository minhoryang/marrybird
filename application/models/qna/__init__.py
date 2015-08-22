"""Look at **TODO**."""
__author__ = 'minhoryang'

from . import (
    questions,
    answers,
#    type,
)

ENABLE_MODELS = [
    ("Q&A", questions, (
        #questions.Question,
    )),
    ("Q&A", answers, (
        #answers.Answer,
    )),
] \
    + []  # XXX : ADD ABOVE