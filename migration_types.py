from sqlalchemy_utils.types.choice import ChoiceType as _ChoiceType

class ChoiceType(_ChoiceType):
    def __init__(self, choices, impl=None, length=255):
        super(__class__, self).__init__(choices, impl)
