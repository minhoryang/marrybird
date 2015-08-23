"""Look at campaigns.Campaign."""
__author__ = 'minhoryang'

from . import (
    questions,
    answers,
    campaigns,
)

ENABLE_MODELS = [
    ("Q&A", questions, (
        questions.Question,
    )),
    ("Q&A", answers, (
        answers.Answer,
    )),
    ("Q&A", campaigns, (
        campaigns.Campaign,
    )),
] \
    + []  # XXX : ADD ABOVE