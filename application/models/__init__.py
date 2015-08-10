from ._base import db

from . import user, record, file, phone, dating

ENABLE_MODELS = [
    ("User", user, (
            user.User,
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
] \
    + dating.ENABLE_MODELS \
    + []  # XXX : ADD ABOVE