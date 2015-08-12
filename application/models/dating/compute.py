__author__ = 'minhoryang'

from .. import db
# TODO : Celery Migration : https://github.com/mitsuhiko/flask-sqlalchemy/issues/332

# TODO : Move out to utils.dating.compute
# It's not a model. isn't it?
def ComputeNow(request_id):
    from ..record import Record
    from .request import Request
    from .met import Met
    from .response import Response

    req = Request.query.get(request_id)
    rec = Record.query.filter(Record.username == req.username).first()

    # Find her/him!
    result = set()
    for i in Record.parse_comma(rec.district_meetable):
        out = Record.query.filter(
            Record.is_male != rec.is_male,
            Record.district_meetable.contains(i),
            Record.age + 4 >= rec.age,
            Record.age - 4 <= rec.age,
            rec._height + 2 >= Record._height if rec.is_male else Record._height + 2 >= rec._height,
            Record.religion == rec.religion if rec.religion != "무교" else True,
        )
        for j in out:
            result.add(j.username)

    # Not met yet.
    result2 = list()
    for i in result:
        out = Met.query.filter(
            Met.A == rec.username,
            Met.B == i
        )
        if not out.first():
            result2.append(i)

    #
    r = Response()
    r.request_id = request_id
    r.username = rec.username
    r.isDone = True
    r.result_json = str(result2)
    db.session.add(r)
    db.session.commit()

    return tuple(result2)

def init(api, jwt):
    pass
