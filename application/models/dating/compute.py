__author__ = 'minhoryang'

from .. import db

# TODO : Move out to utils.dating.compute
# It's not a model. isn't it?
def ComputeNow(request_id):
    from ..record import Record
    from .request import Request
    # read request(request_id)
    req = Request.query.get(request_id)
    rec = Record.query.filter(Record.username == req.username).first()
    meetable = Record.parse_comma(rec.district_meetable)
    for i in meetable:
        out = Record.query.filter(
            Record.is_male != rec.is_male,
            Record.district_meetable.contains(i),
#            Record.parse_age(Record.birthday) + 4 >= Record.parse_age(rec.birthday),
#            Record.parse_age(Record.birthday) - 4 <= Record.parse_age(rec.birthday),
        )
        for j in out:
            print(j.username)
    #Record.query.filter()
    # district_meetable join
    # age +-4
    # height (m+2<f)
    # religion
    pass  # TODO

def init(api, jwt):
    pass