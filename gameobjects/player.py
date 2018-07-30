import tcod

from gameobjects.entity import Entity
from rendering.render_order import RenderOrder


class Player(Entity):
    """ Class for the player object """

    def __init__(self, name, fighter = None, inventory = None):

        super().__init__(0, 0, '@', tcod.white, name, "You.", is_player=True, blocks=True, render_order=RenderOrder.PLAYER, fighter=fighter, inventory=inventory)


    def enemies_in_distance(self, entities, dist=2):
        """ returns nearby monsters in given distance """
        enemies_in_distance = [ent for ent in entities if self.distance_to_ent(ent) <= dist and ent != self and ent.fighter is not None]
        return enemies_in_distance


    def visible_enemies(self, entities, fov_map):
        enemies_in_distance = self.enemies_in_distance(entities, dist=self.fighter.vision)
        visible_enemies = [ent for ent in enemies_in_distance if ent.is_visible(fov_map) and ent != self and ent.fighter is not None]
        return visible_enemies