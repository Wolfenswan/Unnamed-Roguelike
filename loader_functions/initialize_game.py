import logging

from components.actors.fighter import Fighter
from components.inventory import Inventory
from config_files import cfg
from game import Game
from gameobjects.player import Player
from gui.messages import MessageLog
from map.game_map import GameMap
from map.place_actors import place_monsters


def initialize_game(debug=False):

    game = Game(debug=debug)

    # Setup the Player character #
    fighter_component = Fighter(hp=30, defense=2, power=5)
    inventory_component = Inventory(26)
    player = Player('Player', fighter=fighter_component, inventory=inventory_component)

    game.player = player
    game.entities = [player]

    # Setup the game map #
    game.map = GameMap(cfg.MAP_SCREEN_WIDTH, cfg.MAP_SCREEN_HEIGHT)
    game.map.make_map(game, cfg.MAX_ROOMS, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, cfg.MAP_SCREEN_WIDTH, cfg.MAP_SCREEN_HEIGHT, cfg.MAX_ROOM_MONSTERS, cfg.MAX_ROOM_ITEMS)

    place_monsters(game)

    game.message_log = MessageLog(cfg.MSG_X, cfg.MSG_WIDTH, cfg.MSG_HEIGHT)

    return game