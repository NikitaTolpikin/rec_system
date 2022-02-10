import random
from enum import Enum

class EnumChoices(Enum):

    @classmethod
    def choices(cls):
        return [(key.value, key.value) for key in cls]

    @classmethod
    def keys(cls):
        return [key.value for key in cls]

    @classmethod
    def random(cls):
        return random.choice(list(cls.__members__.values()))

    @classmethod
    def get_num(cls, value):
        values_list = [key.value for key in cls]
        assert value in values_list
        return values_list.index(value)

class WarrantyType(EnumChoices):
    NONE = 'Нет'
    ONE_YEAR = '1 год'
    TWO_YEARS = '2 года'
    FIVE_YEARS = '5 лет'