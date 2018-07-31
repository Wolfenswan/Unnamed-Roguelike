import math
from enum import Enum, auto

import tcod

from config_files import colors
from rendering.render_order import RenderOrder


class EntityStates(Enum):
    ENTITY_ACTIVE = auto()
    ENTITY_STUNNED = auto()
    ENTITY_WAITING = auto()


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, descr=None, is_player = False, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, skills=None, item=None, inventory=None):
        self.state = EntityStates.ENTITY_ACTIVE
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.color_bg = None
        self.name = name
        self.descr = descr
        self.is_player = is_player
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.delay_turns = 0
        self.execute_after_delay = None
        self.skills = skills  # dictionary

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.skills is not None:
            for skill in skills.values():
                skill.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def distance_to_ent(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance_to_pos(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

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


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None