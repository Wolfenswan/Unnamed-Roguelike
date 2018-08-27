from enum import Enum, auto

from config_files import cfg
from gui.messages import MessageLog


class GameStates(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    PLAYER_RESTING = auto()
    CURSOR_ACTIVE = auto()
    EQUIPMENT_ACTIVE = auto()
    SHOW_INVENTORY = auto()
    SHOW_EQUIPMENT = auto()
    SHOW_ITEM = auto()
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
        self.turn = 1
        self.state = None
        self.previous_state = None
        self.player_turn_results = []

        # GUI #
        self.con = None
        self.fov_map = None
        self.bottom_panel = None
        self.event_log = MessageLog(cfg.MSG_X, cfg.MSG_WIDTH, cfg.MSG_HEIGHT)
        self.observation_log = MessageLog(cfg.MSG_X, cfg.MSG_WIDTH, cfg.MSG_HEIGHT)