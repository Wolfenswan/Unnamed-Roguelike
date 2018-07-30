import tcod

from gameobjects.entity import Entity
from rendering.render_order import RenderOrder


class Player(Entity):
    """ Class for the player object """

    def __init__(self, name, fighter = None, inventory = None):

        super().__init__(0, 0, '@', tcod.white, name, "You.", is_player=True, blocks=True, render_order=RenderOrder.PLAYER, fighter=fighter, inventory=inventory)

    def enemies_in_distance(self, entities, dist=2):
        """ returns nearby monsters in given distance """
        enemies_in_distance = [ent for ent in entities if ent.distance_to(self) <= dist and ent != self]
        return enemies_in_distance