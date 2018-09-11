from random import randint

from config_files import cfg, colors
from data.data_processing import gen_loadout
from gameobjects.entity import Entity
from gameobjects.player import Player
from map.game_map import GameMap
from map.entity_placement.place_actors import place_monsters
from map.entity_placement.place_architecture import place_staticobjects, place_doors
from map.entity_placement.place_containers import place_containers
from map.entity_placement.place_items import place_items
from rendering.render_order import RenderOrder


def initialize_game(game):

    # Setup the Player character #
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)
    player = Player('Player')
    player_loadouts = { # TODO adapt entries
        'loadout1': {
            'equipment': ('sword','brigandine', 'helmet','belt_generic','shield'),
            'backpack': ('pot_heal', 'scr_fireball','torch', 'spear')
        }
    }
    #loadout = pick_from_data_dict_by_chance(player_loadouts)
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
    place_staticobjects(game)
    place_containers(game)
    place_doors(game)
    place_monsters(game)
    place_items(game)

    player.x, player.y = game.map.rooms[0].center

    return game