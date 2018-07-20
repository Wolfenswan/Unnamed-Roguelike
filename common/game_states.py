from enum import Enum, auto

class GameStates(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    CURSOR_ACTIVE = auto()
    EQUIPMENT_ACTIVE = auto()
    INVENTORY_ACTIVE = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()
