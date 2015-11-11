__author__ = 'minhoryang'

from celery.schedules import crontab


CELERY_BROKER_URL = 'amqp://marrybird:marrybird-localhost@localhost:5672/marrybird'
CELERY_BACKEND_URL = CELERY_BROKER_URL
CELERY_IMPORTS = [
    'application.tasks.user',
    'application.tasks.phone',
    'application.tasks.dating2.action',
    'application.tasks.dating2.event',
    'application.tasks.dating2.state',
    'application.tasks.selfstory',
]
CELERY_ACCEPT_CONTENT = ['json',]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
CELERYBEAT_SCHEDULE = {
    'Every-Day-Im-Shuffling': {
        'task': 'application.tasks.dating2.event.SuggestionAll',
        'schedule': crontab(
            hour='0',
            minute='30',
        ),
    },
    'Rest-In-Peace--Action':{
        'task': 'application.tasks.dating2.action.RestInPeace',
        'schedule': crontab(
            hour='2',
            minute='30'
        ),
    },
    'Rest-In-Peace--Event':{
        'task': 'application.tasks.dating2.event.RestInPeace',
        'schedule': crontab(
            hour='0',
            minute='0'
        ),
    },
    'Rest-In-Peace--State':{
        'task': 'application.tasks.dating2.state.RestInPeace',
        'schedule': crontab(
            hour='3',
            minute='30'
        ),
    },
    'Knock-Knock-Knock-Penny--Are-You-There' : {
        'task': 'application.tasks.dating2.action.NotResponsedAll',
        'schedule': crontab(
            hour='0',
            minute='15',
        ),
    },
}
CELERY_SEND_TASK_SENT_EVENT = True

MARRYBIRD_FLAGS = [
    'celery',
]
