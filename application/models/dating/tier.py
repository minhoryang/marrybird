__author__ = 'minhoryang'

import enum
from functools import lru_cache


class TierType(enum.Enum):
    aA = "aA"
    aB = "aB"
    aC = "aC"
    bB = "bB"
    bC = "bC"
    cC = "cC"

    @staticmethod
    @lru_cache(maxsize=6)
    def getDetails(value):
        return {'external': value[0], 'internal': value[1]}

    @staticmethod
    @lru_cache(maxsize=6)
    def getMatchables(cls, grouping_by='internal'):
        my = __class__.getDetails(cls.value)[grouping_by]

        matchables = list()
        for _value in __class__.__members__:
            if __class__.getDetails(_value)[grouping_by] == my:
                matchables.append(__class__(_value))

        return tuple(matchables)


def init(api, jwt):
    pass  # XXX: No plan