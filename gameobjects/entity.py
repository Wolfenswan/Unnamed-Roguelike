import math
from enum import Enum, auto

import tcod

from components.actionplan import Actionplan
from components.inventory.inventory import Inventory
from components.inventory.paperdoll import Paperdoll
from gameobjects.util_functions import blocking_entity_at_pos
from rendering.render_order import RenderOrder


class EntityStates(Enum):
    ENTITY_ACTIVE = auto()
    ENTITY_STUNNED = auto()
    ENTITY_WAITING = auto()


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, descr=None, type=None, is_player = False, is_corpse = False,
                 blocks=False, blocks_sight = False, render_order=RenderOrder.CORPSE,
                 fighter=None, ai=None, skills=None, item=None, inventory=None, architecture=None):
        self.state = EntityStates.ENTITY_ACTIVE
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.color_bg = None
        self.name = name
        self.descr = descr
        self.type = type
        self.is_player = is_player
        self.is_corpse = is_corpse
        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.render_order = render_order

        # Components #
        self.fighter = fighter
        self.ai = ai
        self.actionplan = Actionplan()
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

    @property
    def pos(self):
        return (self.x, self.y)

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
        if not game.map.is_wall(dest_x, dest_y) or ignore_walls:
            blocked = blocking_entity_at_pos(game.entities, dest_x, dest_y)
            if blocked and not ignore_entities:
                return blocked
            else:
                self.move(dx, dy)
        else:
            return False

    def move_away_from(self, target, game):
        """ Move Entity away from intended target """

        # loop through available directions and pick the first that is at least one square from the player
        # loop does not check for walls, so an entity can back up into walls (and thus fail/be cornered)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                flee_pos = (self.x + dx, self.y + dy)
                distance = target.distance_to_pos(*flee_pos)
                if distance > 1.5:
                    self.try_move(dx, dy, game)
                    break

        # TODO commented part can probably be deleted
        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        # if distance > 2:
        #     dx = int(round(dx / distance))
        #     dy = int(round(dy / distance))

    def distance_to_pos(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to_ent(self, other):
        return self.distance_to_pos(other.x, other.y)

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

        self.actionplan.owner = self



