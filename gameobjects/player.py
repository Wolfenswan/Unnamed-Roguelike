import tcod

from components.actors.fighter import Fighter
from components.inventory.inventory import Inventory
from config_files import cfg
from gameobjects.entity import Entity
from rendering.render_order import RenderOrder


class Player(Entity):
    """ Class for the player object """

    def __init__(self, name):

        fighter_component = Fighter(30, 50, 0, 1, cfg.FOV_RADIUS)
        inventory_component = Inventory(26)

        super().__init__(0, 0, '@', tcod.white, name, descr='This is you.', is_player=True, blocks=True, render_order=RenderOrder.PLAYER, fighter=fighter_component, inventory=inventory_component)


    def enemies_in_distance(self, entities, dist=2):
        """ returns nearby monsters in given distance """
        enemies_in_distance = [ent for ent in entities if self.distance_to_ent(ent) <= dist and ent != self and ent.fighter is not None and not ent.is_corpse]
        return enemies_in_distance

    def visible_enemies(self, entities, fov_map):
        enemies_in_distance = self.enemies_in_distance(entities, dist=self.fighter.vision)
        visible_enemies = [ent for ent in enemies_in_distance if ent.is_visible(fov_map) and ent != self and ent.fighter is not None and not ent.is_corpse]
        return visible_enemies

    def in_combat(self, game):
        visible_enemies = self.visible_enemies(game.entities, game.fov_map)
        if len(visible_enemies) > 0:
            return True
        else:
            return False