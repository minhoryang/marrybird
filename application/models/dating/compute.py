"""<Compute>: Suggest new user by <Request>.

1. Get the <request>
2. Get the requester's information(<record>)
3. Check the following conditions per meet-able districts of the requester.
  - Gender
    + can be tweakable
  - join (Meet-able district)
  - Age +- 4
  - Man's Height +2 >= Woman's Height
  - Same religion (if hasn't, ignore it.)
4. Check already <met>?
5. Then deliver it to <Response>.

READ: Record, Met
GOTO: Response
"""

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
    for i in Record._parse_comma(rec.district_meetable):
        out = Record.query.filter(
            Record.is_male != rec.is_male,
            Record.district_meetable.contains(i),
            Record.age + 4 >= rec.age,
            Record.age - 4 <= rec.age,
            rec._height + 2 >= Record._height if rec.is_male else Record._height + 2 >= rec._height,
            Record.religion == rec.religion if rec.religion != "무교" else True,
        ).all()
        for j in out:
            result.add(j.username)

    # Not met yet.
    result2 = list()
    for i in result:
        out = Met.query.filter(
            Met.A == rec.username,
            Met.B == i
        ).first()
        if not out:
            result2.append(i)

    # TODO : Regular Member.

    r = Response()
    r.request_id = request_id
    r.username = rec.username
    r.isDone = True
    r.result_json = str(result2).replace("'", '"')
    db.session.add(r)
    db.session.commit()
    db.session.close()

    return tuple(result2)
