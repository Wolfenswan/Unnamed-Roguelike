import logging
from random import randint

from components.actors.fighter import Fighter
from components.inventory import Inventory
from config_files import cfg
from game import Game
from gameobjects.player import Player
from gui.messages import MessageLog
from map.game_map import GameMap
from map.place_actors import place_monsters
from map.place_items import place_items


def initialize_game(debug=False):

    game = Game(debug=debug)

    # Setup the Player character #
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Player('Player', fighter=fighter_component, inventory=inventory_component)

    game.player = player
    game.entities = [player]

    # Setup the game map #
    dwidth = randint(cfg.DUNGEON_MIN_WIDTH, cfg.DUNGEON_MAX_WIDTH)
    dheight = randint(cfg.DUNGEON_MIN_HEIGHT, cfg.DUNGEON_MAX_HEIGHT)
    game.map = GameMap(dwidth, dheight)
    game.map.make_map(game, cfg.MAX_ROOMS, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, dwidth, dheight)

    place_monsters(game)
    place_items(game)

    game.message_log = MessageLog(cfg.MSG_X, cfg.MSG_WIDTH, cfg.MSG_HEIGHT)

    return game