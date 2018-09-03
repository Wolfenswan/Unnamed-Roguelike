from random import randint

from components.actors.fighter import Fighter
from components.inventory import Inventory
from config_files import cfg, colors
from data.data_processing import pick_from_data_dict_by_chance, gen_loadout
from gameobjects.entity import Entity
from gameobjects.player import Player
from map.game_map import GameMap
from map.place_actors import place_monsters
from map.place_architecture import place_architecture, place_doors, place_containers
from map.place_items import place_items
from rendering.render_order import RenderOrder


def initialize_game(game):

    # Setup the Player character #
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)
    game.player = Player('Player')
    player_loadouts = {
        'loadout1': {
            'chance': 100,
            'equipment': ('sword_rusty','leather_brittle', 'helmet_rusty','belt_generic','shield_wood'),
            'backpack': ('pot_heal', 'scr_fireball','torch')
        }
    }
    loadout = pick_from_data_dict_by_chance(player_loadouts)
    gen_loadout(game.player, player_loadouts[loadout], game)

    game.entities = [game.player]

    # Setup the game map #
    dwidth = randint(cfg.DUNGEON_MIN_WIDTH, cfg.DUNGEON_MAX_WIDTH)
    dheight = randint(cfg.DUNGEON_MIN_HEIGHT, cfg.DUNGEON_MAX_HEIGHT)
    game.map = GameMap(dwidth, dheight)
    game.map.make_map(game, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, dwidth, dheight)

    # Add the good stuff #
    place_architecture(game)
    place_containers(game)
    place_doors(game)
    #place_items(game)
    place_monsters(game)

    game.player.x, game.player.y = game.map.rooms[0].center()

    return game