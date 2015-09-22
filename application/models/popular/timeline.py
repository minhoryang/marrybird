__author__ = 'minhoryang'

from datetime import datetime, timedelta
from functools import lru_cache, total_ordering

from flask.ext.restplus import Resource
from flask_jwt import jwt_required, current_user
from humanize import naturaltime
from humanize.i18n import activate as humanize

from ..record import Record
from ..selfstory import (
    SelfStory,
    SelfStoryLike,
)
from ..census.question import (
    QuestionBook,
)
from ..census.reply import (
    ReplyBook,
    OldReplyBook,
)
from ..dating2.event import (
    Event_00_Server_Suggested,
    Event_03_AskedOut,
    Event_04_Got_AskedOut,
    Event_05_Got_AskedOut_And_Accept,
    Event_07_AskedOut_Accepted,
    Event_08_EndOfDating,
    Event_09_EndOfDating_And_Feedback,
    Event_99_AskedOut_Rejected,
)


@lru_cache(maxsize=1024)
def CachedUserInfo(username):
    rec = Record.query.filter(
        Record.username == username
    ).first()
    return rec.nickname, rec.photo_thumbnail_url


@lru_cache(maxsize=30)
def CachedQuestionBookTitle(question_book_id):
    qb = QuestionBook.query.get(question_book_id)
    return qb.title


@total_ordering
class TimelineFormat(object):
    username = None
    nickname = None
    photo_thumbnail_url = None

    type = None
    contents = None

    created_at = None
    created_at_humanize = None

    def __init__(self, contents, my_name):
        if isinstance(contents, (ReplyBook, OldReplyBook)):
            self.type = 'census'
            self.username = contents.username
            self.contents = {
                'question_book_title': CachedQuestionBookTitle(contents.question_book_id),
                'question_book_id': contents.question_book_id
            }
            self.created_at = contents.requested_at
        elif isinstance(contents, SelfStory):
            self.type = 'selfstory'
            self.username = contents.username
            self.contents = {
                'selfstory_id': contents.id,
                'selfstory_photo_url': contents.photo_url,
                'title': contents.title if contents.title else contents.story,
            }
            likes = [like.username for like in SelfStoryLike.query.filter(SelfStoryLike.story_id == contents.id).all()]
            self.contents['like_cnt'] = str(len(likes))
            self.contents['liked_already_by_you'] = True if my_name in likes else False
            self.created_at = contents.created_at
        else:
            raise TimelineException()
        self.nickname, self.photo_thumbnail_url = CachedUserInfo(self.username)
        humanize('ko_KR')
        self.created_at_humanize = naturaltime(self.created_at)

    @lru_cache(maxsize=1024)
    def jsonify(self):
        return {
            'username': self.username,
            'nickname': self.nickname,
            'photo_thumbnail_url': self.photo_thumbnail_url,
            'type': self.type,
            'contents': self.contents,
            'created_at': str(self.created_at),
            'created_at_humanize': self.created_at_humanize,
        }

    def __lt__(self, other):
        return self.created_at < other.created_at


def init(**kwargs):
    pass


def module_init(**kwargs):
    api = kwargs['api']
    namespace = kwargs['namespace']
    authorization = api.parser()
    authorization.add_argument('authorization', type=str, required=True, help='"Bearer $JsonWebToken"', location='headers')

    @namespace.route('/timeline')
    class GetTimeline(Resource):

        @jwt_required()
        @api.doc(parser=authorization)
        def get(self):
            username = current_user.username

            people = []
            for SOURCE in (
                Event_00_Server_Suggested,
                Event_09_EndOfDating_And_Feedback,
                Event_08_EndOfDating,
                Event_05_Got_AskedOut_And_Accept,
                Event_07_AskedOut_Accepted,
                Event_04_Got_AskedOut,
                Event_03_AskedOut,
                Event_99_AskedOut_Rejected,
            ):
                for e in SOURCE.query.filter(
                    SOURCE.username == username,
                ).all():
                    people.extend(e._results)
            people = list(set(people))

            contents = []  # TODO : FUCK YOU MINHO, DO IT WITH NOSQL!
            for i in SelfStory.query.filter(
                SelfStory.username.in_(people),
            ).all():
                contents.append(TimelineFormat(i, username))

            question_book_id = []
            for i in ReplyBook.query.filter(
                ReplyBook.username.in_(people),
            ).all():
                if i.question_book_id not in question_book_id:
                    if i.requested_at:
                        contents.append(TimelineFormat(i, username))
                        question_book_id.append(i.question_book_id)

            for i in OldReplyBook.query.filter(
                OldReplyBook.username.in_(people),
            ).all():
                if i.question_book_id not in question_book_id:
                    contents.append(TimelineFormat(i, username))
                    question_book_id.append(i.question_book_id)
            contents.sort(reverse=True)

            return {"status": 200, "message": {i+1: j.jsonify() for i, j in enumerate(contents[:50])}}
