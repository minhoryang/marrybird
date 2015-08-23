from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask.ext.sqlalchemy import SignallingSession as BaseSignallingSession
from flask.ext.sqlalchemy import orm, partial, get_state


class _BindingKeyPattern(object):
    def __init__(self, pattern):
        self.raw_pattern = pattern
        self.compiled_pattern = re.compile(pattern)

    def __repr__(self):
        return "%s<%s>" % (self.__class__.__name__, self.raw_pattern)

    def match(self, key):
        return self.compiled_pattern.match(key)


class _BoundSection(object):
    def __init__(self, db_session_cls, name):
        self.db_session = db_session_cls()
        self.name = name

    def __enter__(self):
        self.db_session.push_binding(self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_session.pop_binding()
        self.db_session.close()


class _SignallingSession(BaseSignallingSession):
    def __init__(self, *args, **kwargs):
        BaseSignallingSession.__init__(self, *args, **kwargs)
        self._binding_keys = []
        self._binding_key = None

    def push_binding(self, key):
        self._binding_keys.append(self._binding_key)
        self._binding_key = key

    def pop_binding(self):
        self._binding_key = self._binding_keys.pop()

    def get_bind(self, mapper, clause=None):
        binding_key = self.__find_binding_key(mapper)
        if binding_key is None:
            return BaseSignallingSession.get_bind(self, mapper, clause)
        else:
            state = get_state(self.app)
            return state.db.get_engine(self.app, bind=binding_key)

    def __find_binding_key(self, mapper):
        if mapper is None: # 맵퍼 없음
            return self._binding_key
        else:
            mapper_info = getattr(mapper.mapped_table, 'info', {})
            mapped_binding_key = mapper_info.get('bind_key')
            if mapped_binding_key: # 맵핑된 바인딩 키 존재
                if type(mapped_binding_key) is str: # 정적 바인딩
                    return mapped_binding_key
                else: # 동적 바인딩
                    if mapped_binding_key.match(self._binding_key): # 현재 바인딩
                        return self._binding_key
                    else: # 푸쉬된 바인딩
                        for pushed_binding_key in reversed(self._binding_keys):
                            if pushed_binding_key and mapped_binding_key.match(pushed_binding_key):
                                return pushed_binding_key
                        else:
                            raise Exception('NOT_FOUND_MAPPED_BINDING:%s CURRENT_BINDING:%s PUSHED_BINDINGS:%s' % (repr(mapped_binding_key), repr(self._binding_key), repr(self._binding_keys[1:])))
            else: # 맵핑된 바인딩 키가 없으면 디폴트 바인딩
                return self._binding_key


class SQLAlchemy(BaseSQLAlchemy):
    def BindingKeyPattern(self, pattern):
        return _BindingKeyPattern(pattern)

    def binding(self, key):
        return _BoundSection(self.session, key)

    def create_scoped_session(self, options=None):
        if options is None:
            options = {}
        scopefunc=options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(_SignallingSession, self, **options), scopefunc=scopefunc
        )

    def get_binds(self, app=None):
        retval = BaseSQLAlchemy.get_binds(self, app)

        bind = None
        engine = self.get_engine(app, bind)
        tables = self.get_tables_for_bind(bind)
        retval.update(dict((table, engine) for table in tables))
        return retval

    def get_tables_for_bind(self, bind=None):
        result = []
        for table in self.Model.metadata.tables.values():
            table_bind_key = table.info.get('bind_key')
            if table_bind_key == bind:
                result.append(table)
            else:
                if bind:
                    if type(table_bind_key) is _BindingKeyPattern and table_bind_key.match(bind):
                        result.append(table)
                    elif type(table_bind_key) is str and table_bind_key == bind:
                        result.append(table)

        return result



db = BaseSQLAlchemy()