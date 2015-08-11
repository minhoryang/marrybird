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
    heightcond = None
    if rec.is_male:
        heightcond = rec._height + 2 >= Record._height
    else:
        heightcond = Record._height + 2 >= rec._height
    religioncond = True
    if rec.religion != "무교":
        religioncond = Record.religion == rec.religion
    result = []
    for i in meetable:
        out = Record.query.filter(
            Record.is_male != rec.is_male,
            Record.district_meetable.contains(i),
            Record.age + 4 >= rec.age,
            Record.age - 4 <= rec.age,
            heightcond,
            religioncond,
        )
        for j in out:
            result.append(j.username)
    for username in set(result):
        print(username)
    # height (m+2<f)
    # religion
    pass  # TODO

def init(api, jwt):
    pass