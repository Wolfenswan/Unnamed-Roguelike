from enum import Enum, auto

from config_files import cfg, colors
from rendering import render_constants as cons
from gameobjects.block_level import BlockLevel
from gui.messages import MessageLog


class GameState(Enum):
    GAME_PAUSED = auto()
    PLAYERS_TURN = auto()
    PLAYER_RESTING = auto()
    CURSOR_ACTIVE = auto()      # Cursor displayed & description window drawn
    CURSOR_TARGETING = auto()   # Cursor displayed & no description window drawn
    EQUIPMENT_ACTIVE = auto()
    SHOW_INVENTORY = auto()
    SHOW_QU_INVENTORY = auto()
    SHOW_EQUIPMENT = auto()
    SHOW_ITEM = auto()
    NPC_TURN = auto()
    PLAYER_DEAD = auto()

# Todo dataclass
class Game:
    def __init__(self, debug=dict):
        self.map = None
        self.dlvl = 1
        self.entities = []

        # Special entities
        self.player = None # Player also has is_player flat set to True
        self.cursor = None
        self.stairs_up = None
        self.stairs_down = None
        self.portal = None

        # Turn Processing #
        self.turn = 1
        self.state = None
        self.previous_state = None
        self.player_turn_results = []

        # GUI #
        self.root = None
        self.fov_map = None
        self.bottom_panel = None
        self.observation_log = MessageLog(cons.MSG_X, cons.MSG_PANEL1_WIDTH, cons.MSG_HEIGHT)
        self.combat_log = MessageLog(cons.MSG_X, cons.MSG_PANEL2_WIDTH, cons.MSG_HEIGHT)

        self.debug = debug

    def toggle_cursor(self, pos=(0,0), state=GameState.CURSOR_ACTIVE):
        if state == GameState.CURSOR_TARGETING:
            self.cursor.color = colors.red
        else:
            self.cursor.color = colors.white

        if self.state == state:
            self.state = self.previous_state
        else:
            self.previous_state = self.state
            self.state = state
            self.cursor.pos = pos

    @property
    def fighter_ents(self):
        ents = [v for v in self.entities if v.fighter is not None]
        return ents

    @property
    def alive_ents(self):
        return [v for v in self.fighter_ents if v.f.hp > 0]

    @property
    def npc_ents(self):
        npc_ents = [v for v in self.fighter_ents if not v.is_player]
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

    @property
    def player_active(self):
        return self.state == GameState.PLAYERS_TURN

    @property
    def npc_active(self):
        return self.state == GameState.NPC_TURN

    @property
    def cursor_active(self):
        return self.state in [GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]
