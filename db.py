"""Code-first Database Implements using SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__MY_DB_FILENAME__ = 'latest.db'
__MY_DB_ENGINE__ = create_engine('sqlite:///%s' % (__MY_DB_FILENAME__,), convert_unicode=True)
SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=__MY_DB_ENGINE__))
__MY_DB_TABLE_BASE__ = declarative_base()
__MY_DB_TABLE_BASE__.query = SESSION.query_property()

from sqlalchemy import Column, Integer, String, Boolean  #, DateTime, ForeignKey
#from sqlalchemy.orm import relationship, backref


class User(__MY_DB_TABLE_BASE__):
    """User object would be mapped with 'users' table."""
    __tablename__ = 'users'

    idx = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True)
    pwd = Column(String(20))  # TODO: Encrypt/Hash/Salt
    gender = Column(Boolean())  # XXX: False-Ladies, True-Gentlemen

    def __init__(self, name, pwd, gender):
        self.name = name
        self.pwd = pwd
        self.gender = gender

    def __repr__(self):
        return self.name


#class Meeting(__MY_DB_TABLE_BASE__):
#    """."""
#    __tablename__ = "meetings"
#
#    idx = Column(Integer, primary_key=True)
#    fromA = Column(Integer, ForeignKey('users.id'))
#    toB = Column(Integer, ForeignKey('users.id'))
#    startedWhen = Column(DateTime)


def init_db(filename=__MY_DB_FILENAME__):
    from os.path import isfile
    if not isfile(filename):
        __MY_DB_TABLE_BASE__.metadata.create_all(bind=__MY_DB_ENGINE__)
