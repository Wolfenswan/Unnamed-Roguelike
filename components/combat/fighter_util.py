from enum import Enum, auto
from typing import Union, Dict


class Stance(Enum):
    DASHING = auto()
    BLOCKING = auto()


class State(Enum):
    DAZED = auto()
    STUNNED = auto()
    ENTANGLED = auto()
    CONFUSED = auto()
    IMMOBILE = auto()

class Surrounded(Enum):
    FREE = auto()
    THREATENED = auto()
    OVERWHELMED = auto()

# class Hindered(Enum):
#     FREE = auto()
#     OBSTRUCTED = auto()
#     BLOCKED = auto()

class AttributePercentage(Enum):
    FULL = 100
    THREE_QUARTER = 75
    HALF = 50
    ONE_QUARTER = 25
    VERY_LOW = 5
    EMPTY = 0


class DamagePercentage(Enum):
    VERY_HIGH = 60
    HIGH = 40
    MODERATE = 20
    LIGHT = 5
    VERY_LIGHT = 1
    NONE = 0


def get_gui_data(percentage:float, dictionary:Dict, category: Union[AttributePercentage, DamagePercentage]):
    """
    Given a percentage value and a dictionary from gui_fighter containing strings or colors, this returns the adequate
    value to display the fighter's status in the GUI.
    """
    for enum in list(category):
        if enum.value <= percentage:
            value = dictionary[enum]
            return value