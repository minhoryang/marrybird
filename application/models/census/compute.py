__author__ = 'minhoryang'

from datetime import datetime

from .. import db


class Compute:
    def __init__(self, record, reply_book, question_book):
        self.record = record
        self.reply_book = reply_book
        self.question_book = question_book
        self._init()

    def run(self):
        raise NotImplementedError()

    def _init(self):
        raise NotImplementedError()


class ComputeException(Exception): pass


class Compute_MBTI(Compute):
    """.

    compute_rules = {
        # Selection : Result
        "A": {"E": 1},
        "B": {"I": 1},
        "C": {"I": 2},

        # Man vs Woman
        "A_Man": {"E": 1},
        "A_Woman": {"E": 2},
        "B_Man": {"I": 2},
        "B_Woman": {"I": 1}
    }
    """
    scores = {
        "E": 0,
        "I": 0,
        "S": 0,
        "N": 0,
        "T": 0,
        "F": 0,
        "J": 0,
        "P": 0,
    }

    def run(self):
        for reply in self.reply_book.iter():
            self._apply_score(reply)
        result = []
        compare = lambda a, b: result.append(a if self.scores[a] >= self.scores[b] else b)
        compare("E", "I")
        compare("S", "N")
        compare("T", "F")
        compare("J", "P")
        return ''.join(result)

    def _init(self):
        self.gender = "Man" if self.record.is_male else "Woman"

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        Selected_R = None

        Possible = [R if reply.answer in R else None for R in CR.keys()]
        for _ in range(Possible.count(None)): Possible.remove(None)
        if len(Possible) == 1:
            Selected_R = Possible[0]
        else:
            Possible = [R if self.gender in R else None for R in Possible]
            for _ in range(Possible.count(None)): Possible.remove(None)
            if len(Possible) == 1:
                Selected_R = Possible[0]
            else:
                raise Exception("Oops")
        for key, value in CR[Selected_R].items():
            if key in self.scores:
                self.scores[key] += value
            else:
                self.scores[key] = value


def ComputeNow(reply_book_id):
    from ..record import Record
    from .reply import ReplyBook
    from .question import QuestionBook

    RB = ReplyBook.query.get(reply_book_id)
    if not RB:
        return 'not found'

    R = Record.query.filter(Record.username == RB.username).first()

    RB.compute_id = reply_book_id  # TODO : CELERY LIVES HERE!
    db.session.add(RB)
    db.session.commit()

    result = "not found"
    QB = QuestionBook.query.get(RB.question_book_id)
    try:
        if QB.compute_type and QB.compute_type in globals():
            result = globals()[QB.compute_type](R, RB, QB).run()
    except ComputeException:
        result = "ComputeException"
    except NotImplementedError:
        result = "NotImplementedError"

    RB.computed_at = datetime.now()
    RB.computed_result = result  # TODO : CALC HOW?
    db.session.add(RB)
    db.session.commit()

    return RB.computed_result
