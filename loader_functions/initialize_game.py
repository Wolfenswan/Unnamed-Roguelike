from random import randint

from config_files import cfg
from config_files import colors
from data.data_keys import Key
from data.data_processing import gen_loadout
from data.data_types import Material, Condition, Craftsmanship
from debug.timer import debug_timer
from gameobjects.entity import Entity
from gameobjects.special_entities import Player
from map.entity_placement.place_actors import place_monsters
from map.entity_placement.place_architecture import place_generic_architecture, place_special_architecture, place_doors
from map.entity_placement.place_containers import place_containers
from map.entity_placement.place_items import place_items
from map.game_map import GameMap
from rendering.render_order import RenderOrder


@debug_timer
def initialize_game(game):
    # Create cursor and the generic projectile entity
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)
    game.projectile = Entity(0, 0, '*', colors.white, 'Projectile', render_order=RenderOrder.NONE)

    initialize_player(game)
    initialize_map(game)

    player = game.player
    player.x, player.y = game.map.rooms[0].center

    initialize_objects(game)

def initialize_player(game):
    # Setup the Player character #
    player = Player('Player')
    player_loadouts = {
        'loadout1': {
            Key.EQUIPMENT: {
                'sword': {
                    Key.MATERIAL: (Material.IRON,),
                    Key.CONDITION: (Condition.NORMAL,),
                    Key.CRAFTSMANSHIP: (Craftsmanship.POOR,)
                },
                'brigandine': {},
                'round_helmet': {},
                'belt': {},
                'round_shield': {}
            },
            Key.BACKPACK: ('pot_heal', 'bomb_1', 'bomb_1', 'torch', 'spear', 'flail', 'bow', 'vest', 'full_helmet')
        }
    }

    gen_loadout(player, player_loadouts['loadout1'], game)
    for item_ent in player.inventory.items + player.paperdoll.equipped_items:
        item_ent.item.identify()

    game.entities.append(player)
    game.player = player
    return player


def initialize_map(game):

    # Setup the game map #
    dwidth = randint(round(cfg.DUNGEON_MIN_WIDTH), round(cfg.DUNGEON_MAX_WIDTH))
    dheight = randint(round(cfg.DUNGEON_MIN_HEIGHT), round(cfg.DUNGEON_MAX_HEIGHT))
    game.map = GameMap(dwidth, dheight)
    game.map.make_map(game, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, dwidth, dheight)


def initialize_objects(game):
    # Add the good stuff #
    place_special_architecture(game)
    place_generic_architecture(game)
    # place_containers(game)
    # place_doors(game)
    # place_items(game)
    # place_monsters(game)


