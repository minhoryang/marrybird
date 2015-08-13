"""Look at .request.Request, It handles all."""
__author__ = 'minhoryang'

from . import request, compute, response, progress, met, review, score, tier

ENABLE_MODELS = [
    ("Dating", request, (
            request.Request,
    )),
    ("Dating", compute, (
    #        compute.Compute,
    )),
    ("Dating", response, (
            response.Response,
    )),
    ("Dating", progress, (
            progress.Progress,
    )),
    ("Dating", met, (
            met.Met,
    )),
    ("Dating", review, (
            review.Review,
    )),
    ("Dating", score, (
            score.Score,
    )),
] \
    + []  # XXX : ADD ABOVE