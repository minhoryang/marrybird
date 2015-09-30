from json import loads
from math import *


HEXACO_JSON = __file__[:-2] + 'json'


class HEXACO_Question:
    def __init__(self):
        self.idx = None
        self.question = None
        self.expected_answer_list = {}
        self.expected_answer_count_max = 0
        self.compute_rules = {}

    def isDone(self):
        if not self.idx:
            raise HEXACO_Exception("No IDX")
        elif not self.question:
            #raise HEXACO_Exception("No Question")
            self.question = ""  # Only Question Can Ignorable.
        elif len(self.expected_answer_list.keys()) == 0:
            raise HEXACO_Exception("No AnswerList")
        elif not self.expected_answer_count_max:
            raise HEXACO_Exception("No Count")
        elif len(self.compute_rules.keys()) == 0:
            raise HEXACO_Exception("No Rules")
        elif len(self.expected_answer_list.keys()) == self.expected_answer_count_max:
            raise HEXACO_Exception("Not Match")

    def convert(self, book_id=None):
        from ..models.census.question import Question

        q = Question()
        if book_id:
            q.book_id = book_id
        q.question = self.question
        q._expected_answers = self.expected_answer_list
        q._compute_rules = self.compute_rules
        q.expected_answer_count = self.expected_answer_count_max
        return q

    @classmethod
    def loads(cls, filename=HEXACO_JSON):
        HEXACO_json = loads(open(filename).read())
        question_keys = list(map(int, HEXACO_json.keys()))
        question_keys.sort()
        if not question_keys == list(range(1,41)):
            raise HEXACO_Exception('Failed to load HEXACO.json')

        questions = []
        for qk in question_keys:
            question = HEXACO_json[str(qk)]
            mq = HEXACO_Question()
            for key, value in question.items():
                if not value:
                    continue
                elif key == 'N':
                    mq.idx = int(value)
                elif key == 'Question':
                    mq.question = value
                elif key == 'MultipleAnswer':
                    mq.expected_answer_count_max = int(value)
                elif '(' in key and ')' in key:  # TODO : WHY DON'T R.E?
                    mq.expected_answer_list[key[1:-1]] = value
                elif key in ['A', 'B', 'C', 'D', 'E']:
                    if int(value[-1]):
                        mq.compute_rules[key] = {value[0:-1]: int(value[-1])}
                elif key == 'Index':
                    mq.compute_rules['Index'] = value
                else:
                    raise HEXACO_Exception('%s %s' % (key, value))
            mq.isDone()
            questions.append(mq)
        return questions

class HEXACO_Exception(Exception):
    pass


def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
        t*(.09678418+t*(-.18628806+t*(.27886807+
        t*(-1.13520398+t*(1.48851587+t*(-.82215223+
        t*.17087277)))))))))
    if (x >= 0.):
        return r
    else:
        return 2. - r


def ncdf(x):
    return 1. - 0.5*erfcc(x/(2**0.5))


def PERCENT(usr, mean, sd):
    return "%.2f" % ((1-ncdf((usr-mean)/sd))*100,)


if __name__ == "__main__":
    # HEXACO_Question.loads()
    #print("%.2f" % PERCENT(4.1, 3.4, 0.7))
    pass