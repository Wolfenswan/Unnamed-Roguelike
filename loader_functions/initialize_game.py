from random import randint

from config_files import cfg, colors
from data.data_processing import gen_loadout, gen_architecture, ARCHITECTURE_DATA_MERGED
from data.data_types import Material, Condition, Craftsmanship
from debug.timer import debug_timer
from gameobjects.entity import Entity
from gameobjects.player import Player
from map.entity_placement.place_actors import place_monsters
from map.entity_placement.place_architecture import place_staticobjects, place_doors
from map.entity_placement.place_containers import place_containers
from map.entity_placement.place_items import place_items
from map.game_map import GameMap
from rendering.render_animations import animate_explosion
from rendering.render_order import RenderOrder

@debug_timer
def initialize_game(game):

    # Setup the Player character #
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)
    game.projectile = Entity(0, 0, '*', colors.white, 'Projectile', render_order=RenderOrder.NONE)
    player = Player('Player')
    player_loadouts = { # TODO adapt entries
        'loadout1': {
            'equipment': {
                'sword': {
                    'materials': (Material.IRON,),
                    'conditions': (Condition.NORMAL,),
                    'craftsmanships': (Craftsmanship.POOR,)
                },
                'brigandine':{},
                'helmet':{},
                'belt_generic':{},
                'round_shield':{}
            },
            'backpack': ('pot_heal', 'bomb_1','bomb_1','bomb_1','torch', 'spear', 'flail', 'bow')
        }
    }

    gen_loadout(player, player_loadouts['loadout1'], game)
    for item_ent in player.inventory.items + player.paperdoll.equipped_items:
        item_ent.item.identify()

    game.entities.append(player)

    # Setup the game map #
    dwidth = randint(cfg.DUNGEON_MIN_WIDTH, cfg.DUNGEON_MAX_WIDTH)
    dheight = randint(cfg.DUNGEON_MIN_HEIGHT, cfg.DUNGEON_MAX_HEIGHT)
    game.map = GameMap(dwidth, dheight)
    game.map.make_map(game, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, dwidth, dheight)

    # Add the good stuff #
    # place_staticobjects(game)
    # place_containers(game)
    # place_doors(game)
    # place_items(game)
    # place_monsters(game)

    player.x, player.y = game.map.rooms[0].center
    p = gen_architecture(ARCHITECTURE_DATA_MERGED['portal'],player.x, player.y)
    game.entities.append(p)

    return game