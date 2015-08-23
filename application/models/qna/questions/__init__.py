""".

I want the Flexible Question System.
With it, Questions are Question Book which includes Question.
(It means that nested-question)
Then how about the answer of above? How to store it?
Did we prepare that? Yes.


"""

__author__ = 'minhoryang'

from sqlalchemy_utils import JSONType

from ... import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = "question_book"
    settings = {}  # db.Column(JSONType)


QuestionTypes = {
    'question_book' : TheQuestionBook,
    'question' : TheQuestion,
}

class TheQuestionRoot:  # TODO : JSON SERIALIZABLE
    """."""
    Title = ""
    Description = ""
    Created_At = ""
    # XXX : NO Modified_At : DO NOT MODIFIED IT! COPY AND CORRECT.
    answer_type = None

    def Serialize(self):
        return __class__._serialize(self)

    @classmethod
    def Deserialize(cls, json):
        return __class__._deserialize(__class__, json)

    def _serialize(self):
        raise NotImplementedYet("Rock Spirit lives here!")

    def _deserialize(self):
        raise NotImplementedYet("There is Spirte Shower!")


class TheQuestionBook(TheQuestionRoot):
    questions = []

    # @override
    answer_type = "nested_questions_answer"


class TheQuestion(TheQuestionRoot):
    pass


def init(api, jwt):
    pass