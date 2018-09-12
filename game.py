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
        self.map = None
        self.dlvl = 1
        self.entities = []

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

        self.debug = {
            'map' : debug,
            'invin': debug
        }

    @property
    def player(self):
        player = next(v for v in self.entities if v.is_player)
        return player

    @property
    def monster_ents(self):
        monster_ents = [v for v in self.entities if v.ai is not None and v.fighter is not None]
        return monster_ents

    @property
    def item_ents(self):
        item_ents = [v for v in self.entities if v.item is not None]
        return item_ents

    @property
    def architecture_ents(self):
        container_ents = [v for v in self.entities if v.architecture is not None]
        return container_ents

    @property
    def container_ents(self):
        container_ents = [v for v in self.entities if v.architecture is not None and v.inventory is not None]
        return container_ents

    @property
    def blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get('walk', False) or v.blocks.get('floor', False)]
        return blocking_ents

    @property
    def walk_blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get('walk', False)]
        return blocking_ents

    @property
    def floor_blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get('floor', False)]
        return blocking_ents