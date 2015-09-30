from json import loads


MBTI_JSON = __file__[:-2] + 'json'


class MBTI_Question:
    def __init__(self):
        self.idx = None
        self.question = None
        self.expected_answer_list = {}
        self.expected_answer_count_max = 0
        self.compute_rules = {}

    def isDone(self):
        if not self.idx:
            raise MBTI_Exception("No IDX")
        elif not self.question:
            #raise MBTI_Exception("No Question")
            self.question = ""  # Only Question Can Ignorable.
        elif len(self.expected_answer_list.keys()) == 0:
            raise MBTI_Exception("No AnswerList")
        elif not self.expected_answer_count_max:
            raise MBTI_Exception("No Count")
        elif len(self.compute_rules.keys()) == 0:
            raise MBTI_Exception("No Rules")
        elif len(self.expected_answer_list.keys()) == self.expected_answer_count_max:
            raise MBTI_Exception("Not Match")

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
    def loads(cls, filename=MBTI_JSON):
        mbti_json = loads(open(filename).read())['MBTI']
        question_keys = list(map(int, mbti_json.keys()))
        question_keys.sort()
        if not question_keys == list(range(1,95)):
            raise MBTI_Exception('Failed to load mbti.json')

        questions = []
        for qk in question_keys:
            question = mbti_json[str(qk)]
            mq = MBTI_Question()
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
                elif key in ['A', 'B', 'C', 'A-Man', 'A-Woman', 'B-Man', 'B-Woman']:
                    if int(value[1]):
                        mq.compute_rules[key] = {value[0]: int(value[1])}
                else:
                    raise MBTI_Exception('%s %s' % (key, value))
            mq.isDone()
            questions.append(mq)
        return questions

    class MBTI_Exception(Exception):
        pass


if __name__ == "__main__":
    MBTI_Question.loads()