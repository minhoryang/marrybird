"""determine the Time/Place/Occasion for showing QnA to specific target users.

The Census.

I want to communicate with my user with this.
When the user didn't finish his profile settings, we can ask him to fill that out by Question System and Push.
What about this dream?

"""

__author__ = 'minhoryang'

from ... import db


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = ""

    created_at = ""

    _type = "broadcast_all"
    _settings = {
        # when it applied (starts, ends)
        # targets define
        # conditions
    }  # db.Column(JSONType)
    question_id = ""

def init(api, jwt):
    pass