from json import loads


class MBTI_Question:
    idx = None
    question = None
    expected_answer_list = {}
    expected_answer_count_max = 0
    compute_rules = {}

    def isDone(self):
        if not self.idx:
            return False
        elif not self.question:
            return False
        elif len(expected_answer_list.keys()) == 0:
            return False
        elif expected_answer_count_max:
            return False
        elif len(compute_rules.keys()) == 0:
            return False
        elif len(expected_answer_list.keys()) == expected_answer_count_max:
            return False
        return True


class MBTI_Exception(Exception):
    pass


if __name__ == "__main__":
    mbti_json = loads(open("mbti.json").read())['MBTI']
    question_keys = list(map(int, mbti_json.keys()))
    question_keys.sort()
    if not question_keys == list(range(1,95)):
        raise MBTI_Exception('Failed to load mbti.json')

    questions = []
    for qk in question_keys:
        question = mbti[qk]
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
                mq.compute_rules[key] = value
            else:
                raise MBTI_Exception('%s %s' % (key, value))