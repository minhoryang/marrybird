"""Look at .request.Request, It handles all."""
__author__ = 'minhoryang'

from . import (
    # request,
    # response,
    # progress,
    met,
    # review,
    # score,
    # tier,
    condition,
)

ENABLE_MODELS = [
    # ("Dating", request, (
    #         request.Request,
    # )),
    # ("Dating", response, (
    #         response.Response,
    # )),
    # ("Dating", progress, (
    #         progress.Progress,
    # )),
    ("Dating", met, (
            met.Met,
            met.Met_Accepted,
            met.Met_Rejected,
            met.Met_NotResponsed,
    )),
    # ("Dating", review, (
    #         review.Review,
    # )),
    # ("Dating", score, (
    #         score.Score,
    # )),
    # ("Dating", tier, (
    # #       tier.Tier,
    # )),
    ("Dating", condition, (
            condition.Condition,
    )),
] \
    + []  # XXX : ADD ABOVE
