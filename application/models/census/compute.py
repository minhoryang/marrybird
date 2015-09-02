__author__ = 'minhoryang'

from datetime import datetime

from .. import db


class Compute:
    def __init__(self, record, reply_book, question_book):
        self.record = record
        self.reply_book = reply_book
        self.question_book = question_book
        self.init()

    def run(self):
        raise NotImplementedError()

    def init(self):
        raise NotImplementedError()

    @staticmethod
    def _rule_reducer(query, rules):
        Possible = [R if query in R else None for R in rules]
        for _ in range(Possible.count(None)):
            Possible.remove(None)
        return Possible

    @staticmethod
    def rule_reducer(queries, rules, chain_and_or='or'):
        Possible = rules
        for query in queries:
            Possible = _rule_reducer(query, Possible)
            if chain_and_or == 'or':
                if len(Possible) == 1:
                    return Possible[0]
            elif chain_and_or == 'and':
                pass
        return Possible


class ComputeException(Exception):
    pass


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
        "E": [],
        "I": [],
        "S": [],
        "N": [],
        "T": [],
        "F": [],
        "J": [],
        "P": [],
    }

    def run(self):
        for reply in self.reply_book.iter():
            self._apply_score(reply)
        result = []
        compare = lambda a, b: result.append(a if sum(self.scores[a]) >= sum(self.scores[b]) else b)
        compare("E", "I")
        compare("S", "N")
        compare("T", "F")
        compare("J", "P")
        return ''.join(result)

    def init(self):
        self.gender = "Man" if self.record.is_male else "Woman"

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        for r in reply.answer:
            Selected_R = rule_reducer(
                (
                    reply.answer,  # try this
                    self.gender,   # then this.
                ),
                CR.keys(),
                chain_and_or='or'
            )
            for mbti_key, mbti_scores in CR[Selected_R].items():
                self.scores[mbti_key].append(mbti_scores)


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
    RB.computed_result = result
    db.session.add(RB)
    db.session.commit()

    return RB.computed_result
