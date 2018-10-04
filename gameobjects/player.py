import tcod

from components.actors.fighter import Fighter
from components.inventory.inventory import Inventory
from config_files import cfg
from gameobjects.block_level import BlockLevel
from gameobjects.entity import Entity
from rendering.render_order import RenderOrder


class Player(Entity):
    """ Class for the player object """

    def __init__(self, name):

        fighter_component = Fighter(60, 120, 0, 2, cfg.FOV_RADIUS)
        inventory_component = Inventory(capacity=26)
        print(inventory_component)

        super().__init__(0, 0, '@', tcod.white, name, descr='This is you.', is_player=True,
                         blocks={BlockLevel.WALK:True}, render_order=RenderOrder.PLAYER,
                         fighter=fighter_component, inventory=inventory_component)