__author__ = 'minhoryang'

from datetime import datetime
from hashlib import md5

from ._hexaco import *
from .. import db
from ...externals.HEXACO import PERCENT as HEXACO_PERCENT


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
            Possible = Compute._rule_reducer(query, Possible)
            if chain_and_or == 'or':
                if len(Possible) == 1:
                    return Possible[0]
            elif chain_and_or == 'and':
                pass
        return Possible


class ComputeException(Exception):
    pass


class Compute_Test(Compute):
    def init(self):
        pass

    def run(self):
        for reply in self.reply_book.iter():
            print((reply._answers, type(reply._answers)))
        return 'check console'


class Compute_Hash(Compute):
    """ResultBook will Hash You!"""
    def init(self):
        from .result import ResultBook
        self.values = ResultBook.query.filter(
            ResultBook.question_book_id == self.question_book.id
        ).all()

    def run(self):
        target = ""
        for reply in self.reply_book.iter():
            target += str(reply._answers)
        key = int(md5(target.encode("utf-8")).hexdigest(), 16)
        key %= len(self.values)
        return self.values[key].result


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
        compare("N", "S")  # N>=S
        compare("F", "T")  # F>=T
        compare("P", "J")  # P>=J
        return ''.join(result)

    def init(self):
        self.gender = "Man" if self.record.is_male else "Woman"

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        for r in reply._answers:
            Selected_R = Compute.rule_reducer(
                (
                    r,  # try this
                    self.gender,   # then this.
                ),
                CR.keys(),
                chain_and_or='or'
            )
            if Selected_R:
                for mbti_key, mbti_scores in CR[Selected_R].items():
                    self.scores[mbti_key].append(mbti_scores)


class Compute_HEXACO(Compute):
    def run(self):
        for reply in self.reply_book.iter():
            self._apply_score(reply)

        Total = []
        for key in self.scores:
            Total.extend(self.scores[key])
        self.scores['Total'] = Total

        Result = {}
        for key in self.result_rules:
            Result[key] = HEXACO_PERCENT(sum(self.scores[key])/self.result_rules[key]['cnt'], self.result_rules[key]['avg'], self.result_rules[key]['sd'])

        return str(Result)  # jsonify

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        for r in reply._answers:
            Selected_R = Compute.rule_reducer(
                (
                    r,
                ),
                CR.keys(),
                chain_and_or='or'
            )
            if Selected_R:
                for key, scores in CR[Selected_R].items():
                    self.scores[key].append(scores)


class Compute_HEXACO_H(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_H['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_H['result_rules']


class Compute_HEXACO_E(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_E['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_E['result_rules']


class Compute_HEXACO_X(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_X['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_X['result_rules']


class Compute_HEXACO_A(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_A['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_A['result_rules']


class Compute_HEXACO_C(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_C['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_C['result_rules']


class Compute_HEXACO_O(Compute_HEXACO):
    def init(self):
        self.scores = {}
        for i in HEXACO_O['result_rules']:
            if not i == 'Total':
                self.scores[i] = []
        self.result_rules = HEXACO_O['result_rules']


class Compute_O_H(Compute):
    def run(self):
        for reply in self.reply_book.iter():
            self._apply_score(reply)

        return str(sum(self.scores['C']))

    def init(self):
        self.scores = {'C': []}

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        for r in reply._answers:
            Selected_R = Compute.rule_reducer(
                (
                    r,
                ),
                CR.keys(),
                chain_and_or='or'
            )
            if Selected_R:
                for key, scores in CR[Selected_R].items():
                    self.scores[key].append(scores)


class Compute_NARC(Compute):
    def run(self):
        for reply in self.reply_book.iter():
            self._apply_score(reply)

        return str(sum(self.scores['C']))

    def init(self):
        self.scores = {'C': []}

    def _apply_score(self, reply):
        CR = reply.getQuestion()._compute_rules
        for r in reply._answers:
            Selected_R = Compute.rule_reducer(
                (
                    r,
                ),
                CR.keys(),
                chain_and_or='or'
            )
            if Selected_R:
                for key, scores in CR[Selected_R].items():
                    self.scores[key].append(scores)


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

    return result  # XXX : After db.session.close() you can't use the variables from DB.
