__author__ = 'minhoryang'

from datetime import datetime
from hashlib import md5

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

        def percent(score, rule):
            avg, sd = rule
            # TODO FILL IN
            return score

        Result = {}
        for key in self.result_rules:
            Result[key] = percent(self.scores[key], self.result_rules[key])

        return Result  # jsonify

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
        self.scores = {
            'H:Sinc': [],
            'H:Fair': [],
            'H:Gree': [],
            'H:Mode': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.91,
                'sd': 0.46,
            },
            'H:Sinc': {
                'avg': 3.79,
                'sd': 0.57,
            },
            'H:Fair': {
                'avg': 4.26,
                'sd': 0.58,
            },
            'H:Gree': {
                'avg': 3.71,
                'sd': 0.64,
            },
            'H:Mode': {
                'avg': 3.88,
                'sd': 0.61,
            },
        }


class Compute_HEXACO_E(Compute_HEXACO):
    def init(self):
        self.scores = {
            'E:Fear': [],
            'E:Anxi': [],
            'E:Depe': [],
            'E:Sent': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.19,
                'sd': 0.47,
            },
            'E:Fear': {
                'avg': 3.05,
                'sd': 0.69,
            },
            'E:Anxi': {
                'avg': 3.12,
                'sd': 0.72,
            },
            'E:Depe': {
                'avg': 2.93,
                'sd': 0.62,
            },
            'E:Sent': {
                'avg': 3.65,
                'sd': 0.61,
            },
        }


class Compute_HEXACO_X(Compute_HEXACO):
    def init(self):
        self.scores = {
            'X:Expr': [],
            'X:SocB': [],
            'X:Soci': [],
            'X:Live': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.19,
                'sd': 0.53,
            },
            'X:Expr': {
                'avg': 2.89,
                'sd': 0.71,
            },
            'X:SocB': {
                'avg': 3.16,
                'sd': 0.76,
            },
            'X:Soci': {
                'avg': 3.12,
                'sd': 0.67,
            },
            'X:Live': {
                'avg': 3.6,
                'sd': 0.62,
            },
        }


class Compute_HEXACO_A(Compute_HEXACO):
    def init(self):
        self.scores = {
            'A:Forg': [],
            'A:Gent': [],
            'A:Flex': [],
            'A:Pati': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.13,
                'sd': 0.47,
            },
            'A:Forg': {
                'avg': 2.87,
                'sd': 0.65,
            },
            'A:Gent': {
                'avg': 3.19,
                'sd': 0.6,
            },
            'A:Flex': {
                'avg': 3.07,
                'sd': 0.54,
            },
            'A:Pati': {
                'avg': 3.38,
                'sd': 0.62,
            },
        }


class Compute_HEXACO_C(Compute_HEXACO):
    def init(self):
        self.scores = {
            'C:Orga': [],
            'C:Dili': [],
            'C:Perf': [],
            'C:Prud': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.58,
                'sd': 0.45,
            },
            'C:Orga': {
                'avg': 3.6,
                'sd': 0.79,
            },
            'C:Dili': {
                'avg': 3.55,
                'sd': 0.6,
            },
            'C:Perf': {
                'avg': 3.57,
                'sd': 0.55,
            },
            'C:Prud': {
                'avg': 3.6,
                'sd': 0.54,
            },
        }


class Compute_HEXACO_O(Compute_HEXACO):
    def init(self):
        self.scores = {
            'O:AesA': [],
            'O:Inqu': [],
            'O:Crea': [],
            'O:Unco': [],
        }
        self.result_rules = {
            'Total': {
                'avg': 3.39,
                'sd': 0.53,
            },
            'O:AesA': {
                'avg': 3.64,
                'sd': 0.69,
            },
            'O:Inqu': {
                'avg': 3.64,
                'sd': 0.68,
            },
            'O:Crea': {
                'avg': 3.17,
                'sd': 0.72,
            },
            'O:Unco': {
                'avg': 3.11,
                'sd': 0.66,
            },
        }


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
