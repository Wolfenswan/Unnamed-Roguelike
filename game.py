from enum import Enum, auto

class GameStates(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    PLAYER_RESTING = auto()
    CURSOR_ACTIVE = auto()
    EQUIPMENT_ACTIVE = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    ENEMY_TURN = auto()
    TARGETING = auto()
    PLAYER_DEAD = auto()

class Game:
    def __init__(self, debug=False):
        self.debug = debug
        self.map = None
        self.dlvl = 1
        self.player = None
        self.entities = None

        # Turn Processing #
        self.state = None
        self.previous_state = None
        self.player_turn_results = []

        # GUI #
        self.con = None
        self.bottom_panel = None
        self.message_log = None