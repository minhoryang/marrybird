"""Look at .request.Request, It handles all."""
__author__ = 'minhoryang'

from . import (
    request,
    response,
    progress,
    met,
    review,
    score,
    tier,
)

ENABLE_MODELS = [
    ("Dating", request, (
            request.Request,
    )),
    ("Dating", response, (
            response.Response,
    )),
    ("Dating", progress, (
            progress.Progress,
    )),
    ("Dating", met, (
            met.Met,
            met.Met_Accepted,
            met.Met_Rejected,
    )),
    ("Dating", review, (
            review.Review,
    )),
    ("Dating", score, (
            score.Score,
    )),
    ("Dating", tier, (
    #       tier.Tier,
    )),
] \
    + []  # XXX : ADD ABOVE