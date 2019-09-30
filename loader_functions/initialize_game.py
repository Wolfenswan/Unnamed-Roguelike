from random import randint, choice

from config_files import cfg
from config_files import colors
from data.actor_data import act_classes
from data.data_keys import Key
from data.data_processing import gen_loadout
from debug.timer import debug_timer
from gameobjects.entity import Entity
from gameobjects.special_entities import Player
from map.entity_placement.place_actors import place_monsters
from map.entity_placement.place_architecture import place_generic_architecture, place_special_architecture, place_doors
from map.entity_placement.place_containers import place_containers
from map.entity_placement.place_items import place_items
from map.entity_placement.place_uniques import place_uniques
from map.game_map import GameMap
from rendering.render_order import RenderOrder
from rendering.util_functions import print_string


@debug_timer
def initialize_game(game):
    game.turn = 1
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)
    game.projectile = Entity(0, 0, '*', colors.white, 'Projectile', render_order=RenderOrder.NONE)

    initialize_player(game)
    initialize_map(game)

    player = game.player
    player.x, player.y = game.map.rooms[0].center

    initialize_objects(game)

def initialize_player(game):
    # Setup the Player character #
    p_data = act_classes.classes_data['generic']
    player = Player('Player', p_data)

    loadout = choice(list(p_data[Key.LOADOUTS].values()))
    gen_loadout(player, loadout)
    for item_ent in player.inventory.items + player.paperdoll.equipped_items:
        item_ent.item.identify()

    game.entities = [player]
    game.player = player
    return player


def initialize_map(game):

    # Setup the game map #
    dwidth = randint(round(cfg.DUNGEON_MIN_WIDTH), round(cfg.DUNGEON_MAX_WIDTH))
    dheight = randint(round(cfg.DUNGEON_MIN_HEIGHT), round(cfg.DUNGEON_MAX_HEIGHT))
    game.map = GameMap(dwidth, dheight)
    game.map.create_map(cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE)

    return game.map

def initialize_objects(game):
    # Add the good stuff #
    place_special_architecture(game)
    place_uniques(game)
    if not game.debug['prevent_npc_spawning']:
        place_monsters(game)
    if not game.debug['prevent_item_spawning']:
        place_items(game)
        place_containers(game)
    if not game.debug['prevent_architecture_spawning']:
        place_generic_architecture(game)
        place_doors(game)


