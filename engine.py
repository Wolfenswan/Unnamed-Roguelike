import tcod

from components.actors.fighter import Fighter
from game import Game
from gameobjects.entity import Entity, get_blocking_entities_at_location
from common import config as cfg, colors
from common.game_states import GameStates
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_functions import clear_all, render_all, RenderOrder, initialize_window
from input.handle_keys import handle_keys
from map.game_map import GameMap


def initialize_game():

    screen_width = cfg.SCREEN_WIDTH
    screen_height = cfg.SCREEN_HEIGHT
    bar_width = 20
    panel_height = cfg.BOTTOM_PANEL_HEIGHT
    panel_y = cfg.BOTTOM_PANEL_Y
    map_width = cfg.SCREEN_WIDTH
    map_height = cfg.MAP_SCREEN_HEIGHT
    room_max_size = cfg.ROOM_MAX_SIZE
    room_min_size = cfg.ROOM_MIN_SIZE
    max_rooms = cfg.MAX_ROOMS
    max_monsters_per_room = cfg.MAX_ROOM_MONSTERS

    game = Game()

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, is_player = True)
    entities = [player]

    game.player = player

    initialize_window()

    con = tcod.console_new(screen_width, screen_height)
    panel = tcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_map = initialize_fov(game_map)

    game_loop(con, panel, player, entities, game_map, fov_map)

def game_loop(con, panel, player, entities, game_map, fov_map):

    game_state = GameStates.PLAYERS_TURN
    fov_recompute = True

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute)

        fov_recompute = False

        tcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # Player moves #
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # Results of Player actions #
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                message = dead_entity.fighter.death()
                if dead_entity.is_player:
                    game_state = GameStates.PLAYER_DEAD

                print(message)

        # Enemies take turns #
        if game_state == GameStates.ENEMY_TURN:
            # move_order = sorted(entities, key=lambda i: i.distance_to(player))
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            message = dead_entity.fighter.death()
                            if dead_entity.is_player:
                                game_state = GameStates.PLAYER_DEAD

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    initialize_game()