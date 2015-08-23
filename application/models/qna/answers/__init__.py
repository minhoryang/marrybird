""".

The Feedback.

The answer will be different caused by the user, the time, ...
I want to cover it all.

"""

__author__ = 'minhoryang'

from ... import db
from .questions import Question, QuestionTypes

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = ""
    modified_at = ""

    type = ""
    settings = {}  # db.column(JSONType)
    campaign_id = ""
    the_answer = {
        "question_id": "answer",
    }  # db.column(JSONType)


class TheAnswerRoot:
    """Deserialize만 고려하면되지?."""
    @staticmethod
    def the_answer(json):
        for key, value in json:  # TODO : WILL WORK.
            yield QuestionTypes[Question.query.get(key).type].Deserialize(value)
            # TODO ????
        return __class__._deserialize(__class__, json)

    def _deserialize(self, json):  # TODO : static?
        raise NotImplementedYet()


class Nested_Question_Answer(TheAnswerRoot):
    """

    the_answer = {
      "question_id" : {
        "value": "the_answer_of_question",
      }
    }
    """  # answer의 type을 지정해 주는것이 좋은가?
         # 파싱할땐 빠르겠지. 클라가 응답할땐?

    # @Override
    def _deserialize(self, json):



def init(api, jwt):
    pass