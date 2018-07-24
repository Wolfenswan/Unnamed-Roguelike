from enum import Enum, auto

class RenderOrder(Enum):
    """ the RenderOrder class is a component of all objects and determines their render priority """

    NONE = auto()
    BOTTOM = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
    PLAYER = auto()
    CURSOR = auto()