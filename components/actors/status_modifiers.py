from enum import Enum, auto

class Presence(Enum):
    NORMAL = auto()
    DAZED = auto()
    STUNNED = auto()

class Surrounded(Enum):
    FREE = auto()
    THREATENED = auto()
    OVERWHELMED = auto()