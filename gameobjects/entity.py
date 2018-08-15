import math
from enum import Enum, auto

import tcod

from components.inventory import Inventory
from components.paperdoll import Paperdoll
from components.actors.turnplan import Turnplan
from gameobjects.util_functions import get_blocking_entity_at_location
from rendering.render_order import RenderOrder


class EntityStates(Enum):
    ENTITY_ACTIVE = auto()
    ENTITY_STUNNED = auto()
    ENTITY_WAITING = auto()


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, descr=None, is_player = False, is_corpse = False, blocks=False, blocks_sight = False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, skills=None, item=None, inventory=None, architecture=None):
        """

        :param x: pos x
        :type x: int
        :param y: pos y
        :type y: int
        :param char: ascii character
        :type char: str
        :param color: color
        :type color: tuple
        :param name: entity name
        :type name: str
        :param is_player: is_player flag
        :type is_player: bool
        :param blocks: blocks flag
        :type blocks: bool
        :param render_order:
        :type render_order: RenderOrder
        :param fighter:
        :type fighter:
        :param ai:
        :type ai:
        :param skills:
        :type skills:
        :param item:
        :type item:
        :param inventory:
        :type inventory:

        """
        self.state = EntityStates.ENTITY_ACTIVE
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.color_bg = None
        self.name = name
        self.descr = descr
        self.is_player = is_player
        self.is_corpse = is_corpse
        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.render_order = render_order

        # Components #
        self.fighter = fighter
        self.ai = ai
        self.turnplan = Turnplan()
        self.item = item
        self.inventory = inventory
        if self.inventory:
            self.paperdoll = Paperdoll()
            self.qu_inventory = Inventory(capacity = 0)
        self.skills = skills  # dictionary
        self.architecture = architecture
        self.set_ownership() # Sets ownership for all components

        # AI related attributes #
        self.delay_turns = 0
        self.execute_after_delay = None

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def try_move(self, dx, dy, game, ignore_entities=False, ignore_walls = False):
        """
        Attempts to move the entity in the given direction.
        If the direction is blocked by another entity, the blocking entity is returned.
        If the direction is non-walkable, False is returned

        """
        dest_x, dest_y = self.x + dx, self.y + dy
        if not game.map.is_blocked(dest_x, dest_y) or ignore_walls:
            blocked = get_blocking_entity_at_location(game.entities, dest_x, dest_y)
            if blocked and not ignore_entities:
                return blocked
            else:
                self.move(dx, dy)
        else:
            return False

    def move_away_from(self, target):
        """ Move Entity away from intended target """
        # TODO: improve so all that it always moves to a tile that it is at least 1 tile distance from the player
        dx, dy = (0, 0)

        # loop through available directions and pick the first that is at least one space from the player
        # loop does not check for walls, as monster can back up into walls (and thus fail)
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                flee_pos = (self.x + x, self.y + y)
                if target.distance_to_pos(*flee_pos) > 1.5:
                    (dx, dy) = (x, y)
                    break

        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        if distance:
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

        self.move(dx, dy)

    def distance_to_ent(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance_to_pos(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def direction_to_pos(self, x, y):
        dx, dy = 0, 0
        x_plane = x - self.x
        y_plane = y - self.y

        if x_plane > 0:
            dx = 1
        elif x_plane < 0:
            dx = -1

        if y_plane > 0:
            dy = 1
        elif y_plane < 0:
            dy = -1

        return dx, dy

    def direction_to_ent(self, other):
        dx, dy = 0, 0
        x_plane = other.x - self.x
        y_plane = other.y - self.y

        if x_plane > 0:
            dx = 1
        elif x_plane < 0:
            dx = -1

        if y_plane > 0:
            dy = 1
        elif y_plane < 0:
            dy = -1

        return dx, dy

    def same_pos_as(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def is_visible(self, fov_map):
        return tcod.map_is_in_fov(fov_map, self.x, self.y)

    def available_skills(self, game):
        available_skills = [skill for skill in self.skills.values() if skill.is_available(game)]
        return available_skills

    def cooldown_skills(self, reset=False):
        for skill in self.skills.values():
            skill.cooldown_skill(reset=reset)

    def get_nearby_entities(self, game, ai_only=False, dist=2, filter_player = True):
        """ returns nearby entitis in given distance """
        # TODO bugfix & check perfomance
        entities_in_range = [ent for ent in game.entities if ent.distance_to_ent(self) <= dist and ent != self and (ai_only and ent.ai is not None) and (filter_player and ent.is_player == False)]
        #entities_in_range.sort(key=self.distance_to_ent)
        print(entities_in_range)
        return entities_in_range

    def set_ownership(self):
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self
            self.paperdoll.owner = self
            self.qu_inventory.owner = self

        if self.architecture:
            self.architecture.owner = self

        if self.skills is not None:
            for skill in self.skills.values():
                skill.owner = self

        self.turnplan.owner = self



