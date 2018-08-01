import logging
from random import randint

from components.actors.fighter import Fighter
from components.inventory import Inventory
from config_files import cfg, colors
from game import Game
from gameobjects.entity import Entity
from gameobjects.player import Player
from gui.messages import MessageLog
from map.game_map import GameMap
from map.place_actors import place_monsters
from map.place_items import place_items
from rendering.render_order import RenderOrder


def initialize_game(debug=False):

    game = Game(debug=debug)

    # Setup the Player character #
    fighter_component = Fighter(hp=30, defense=2, power=5, vision=cfg.FOV_RADIUS)
    inventory_component = Inventory(26)
    game.player = Player('Player', fighter=fighter_component, inventory=inventory_component)
    game.cursor = Entity(0, 0, 'X', colors.white, 'Cursor', render_order=RenderOrder.CURSOR)

    game.entities = [game.player]

    # Setup the game map #
    dwidth = randint(cfg.DUNGEON_MIN_WIDTH, cfg.DUNGEON_MAX_WIDTH)
    dheight = randint(cfg.DUNGEON_MIN_HEIGHT, cfg.DUNGEON_MAX_HEIGHT)
    game.map = GameMap(dwidth, dheight)
    game.map.make_map(game, cfg.MAX_ROOMS, cfg.ROOM_MIN_SIZE, cfg.ROOM_MAX_SIZE, dwidth, dheight)

    #place_monsters(game)
    place_items(game)

    game.message_log = MessageLog(cfg.MSG_X, cfg.MSG_WIDTH, cfg.MSG_HEIGHT)

    return game