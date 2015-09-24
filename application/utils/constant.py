__author__ = 'minhoryang'

from os import mkdir as _mkdir
from os.path import join


SQLALCHEMY_BINDS_RULES = lambda project_path, category, name, flags: {name: SQLALCHEMY_DATABASE_URI(name, project_path, category, flags)}


def SQLALCHEMY_DATABASE_URI(name, project_path=None, category=None, flags=None):
    if not flags:
        flags = []
    if 'postgresql' in flags:
        return 'postgresql://marrybird:marrybird-localhost@marrybird.crhhlrdtvvdm.ap-northeast-1.rds.amazonaws.com/%s' % (name, )
    elif 'sqlite' in flags:
        path = mkdir(join(project_path, 'db'))
        path = mkdir(join(path, category))
        return 'sqlite:///%s/%s.db' % (path, name)
    raise Exception('No DB in flags')


def mkdir(dir):
    dir = dir.replace(' ', '_')
    try:
        _mkdir(dir)
    except FileExistsError:
        pass
    return dir
