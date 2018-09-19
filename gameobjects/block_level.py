from enum import Enum, auto

class BlockLevel(Enum):
    """
    BlockLevel defines what the entity can/will block when another entity moves into it, FOV is rendered or what the
    Entity is blocked by when moving itself or being placed. It is assigned to every entity via the Entity blocks
    attribute (dictionary).
    """
    WALK = auto()
    FLOOR = auto()
    SIGHT = auto()