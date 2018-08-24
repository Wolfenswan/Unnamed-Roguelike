from enum import Enum, auto

class RenderOrder(Enum):
    """ the RenderOrder class is a component of all objects and determines their render priority """

    NONE = auto()
    CORPSE = auto()
    BOTTOM = auto()
    ITEM = auto()
    ACTOR = auto()
    PLAYER = auto()
    CURSOR = auto()
    ALWAYS = auto()