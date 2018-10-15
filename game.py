from enum import Enum, auto

from config_files import cfg
from gameobjects.block_level import BlockLevel
from gui.messages import MessageLog


class GameState(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    PLAYER_RESTING = auto()
    CURSOR_ACTIVE = auto()
    EQUIPMENT_ACTIVE = auto()
    SHOW_INVENTORY = auto()
    SHOW_QU_INVENTORY = auto()
    SHOW_EQUIPMENT = auto()
    SHOW_ITEM = auto()
    ENEMY_TURN = auto()
    PLAYER_DEAD = auto()

class Game:
    def __init__(self, debug=False):
        self.map = None
        self.cursor = None
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
        self.observation_log = MessageLog(cfg.MSG_X, cfg.MSG_PANEL1_WIDTH, cfg.MSG_HEIGHT)
        self.combat_log = MessageLog(cfg.MSG_X, cfg.MSG_PANEL2_WIDTH, cfg.MSG_HEIGHT)

        self.debug = {
            'map' : debug,
            'invin': debug,
            'ent_info': debug
        }

    def toggle_cursor(self, pos=(0,0), state=GameState.CURSOR_ACTIVE):
        if self.state == state:
            self.state = self.previous_state
        else:
            self.previous_state = self.state
            self.state = state
            self.cursor.pos = pos

    @property
    def player(self):
        player = next(v for v in self.entities if v.is_player)
        return player

    @property
    def fighter_ents(self):
        ents = [v for v in self.entities if v.fighter is not None]
        return ents

    @property
    def alive_ents(self):
        return [v for v in self.fighter_ents if v.fighter.hp > 0]

    @property
    def npc_ents(self):
        npc_ents = [v for v in self.fighter_ents if v.ai is not None]
        return npc_ents

    @property
    def item_ents(self):
        item_ents = [v for v in self.entities if v.item is not None]
        return item_ents

    @property
    def architecture_ents(self):
        container_ents = [v for v in self.entities if v.architecture is not None]
        return container_ents

    @property
    def interactable_ents(self):
        interactable_ents = [v for v in self.architecture_ents if v.architecture.on_interaction is not None]
        return interactable_ents

    @property
    def container_ents(self):
        container_ents = [v for v in self.architecture_ents if v.inventory is not None]
        return container_ents

    @property
    def blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get(BlockLevel.WALK, False) or v.blocks.get(BlockLevel.FLOOR, False)]
        return blocking_ents

    @property
    def walk_blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get(BlockLevel.WALK, False)]
        return blocking_ents

    @property
    def sight_blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get(BlockLevel.SIGHT, False)]
        return blocking_ents

    @property
    def floor_blocking_ents(self):
        blocking_ents = [v for v in self.entities if v.blocks.get(BlockLevel.FLOOR, False)]
        return blocking_ents