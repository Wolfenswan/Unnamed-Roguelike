import math

from rendering.fov_functions import pos_is_visible
from rendering.render_order import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, descr=None, is_player = False, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.descr = descr
        self.is_player = is_player
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

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


    def can_see_ent(self, fov_map, other):
        return pos_is_visible(fov_map, other.x, other.y)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None