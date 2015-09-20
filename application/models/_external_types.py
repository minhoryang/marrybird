from enum import Enum

from sqlalchemy_utils import (
    ChoiceType,
    ScalarListType,
    JSONType,
    UUIDType,
)


class EnumType(ChoiceType):
    def copy(self, **kargs):
        if 'schema' in kargs:
            kargs.pop('schema')
        return super(__class__, self).copy(**kargs)
