from ._base import db

from . import (
    user,
    record,
    file,
    phone,
    selfstory,
    notice,
    tomarrybird,
)

from .dating import ENABLE_MODELS as DATING_ENABLE_MODELS
from .dating2 import ENABLE_MODELS as DATING2_ENABLE_MODELS
from .census import ENABLE_MODELS as CENSUS_ENABLE_MODELS

ENABLE_MODELS = [
    ("User", user, (
            user.MaleUser,
            user.FemaleUser,
    )),
    ("User", record, (
            record.Record,
    )),
    ("User", file, (
            file.File,
    )),
    ("User", phone, (
            phone.Phone,
    )),
    ("User", selfstory, (
            selfstory.SelfStory,
            selfstory.SelfStoryLike,
    )),
    ("User", notice, (
            notice.Notice,
    )),
    ("User", tomarrybird, (
            tomarrybird.ToMarrybird,
    )),
] \
    + DATING_ENABLE_MODELS \
    + DATING2_ENABLE_MODELS \
    + CENSUS_ENABLE_MODELS \
    + []  # XXX : ADD ABOVE
