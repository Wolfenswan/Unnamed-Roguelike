import tcod

from game import GameStates
from gameobjects.entity import get_blocking_entities_at_location
from gui.menus import inventory_menu
from gui.messages import Message, MessageType
from input.handle_input import handle_keys, handle_mouse
from input.process_input import process_input
from loader_functions.initialize_game import initialize_game
from loader_functions.initialize_logging import initialize_logging
from loader_functions.initialize_window import initialize_window
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import clear_all, render_all
from rendering.common_functions import pos_on_screen


def game_loop(game, fov_map):
    player = game.player
    entities = game.entities
    con = game.con
    message_log = game.message_log

    game.state = GameStates.PLAYERS_TURN
    game.previous_state = game.state

    targeting_item = None

    fov_recompute = True

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        # tcod.sys_set_fps(30)
        # tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)

        render_all(game, fov_map, mouse)

        fov_recompute = False

        tcod.console_flush()

        clear_all(con, entities)

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse, True)

        action = handle_keys(key, game.state)
        mouse_action = handle_mouse(mouse)

        game.player_turn_results = process_input(action, mouse_action, fov_map, game, targeting_item = targeting_item)

        # Results of Player actions #
        for player_turn_result in game.player_turn_results:
            message = player_turn_result.get('message')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            dead_entity = player_turn_result.get('dead')
            targeting_item = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            resting = player_turn_result.get('resting')

            # List of results that activate the enemy's turn #
            enemy_turn_on = [item_added, item_dropped, item_consumed]

            if message:
                message_log.add_message(message)

            if dead_entity:
                message = dead_entity.fighter.death(game.map)
                if dead_entity.is_player:
                    game.state = GameStates.PLAYER_DEAD

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

            if item_dropped:
                entities.append(item_dropped)

            # Enable enemy turn if at least one of the results is valid
            filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
            if len(filtered_enemy_turn_conditions) > 0:
                game.state = GameStates.ENEMY_TURN

            if targeting_item:
                game.previous_state = GameStates.PLAYERS_TURN
                game.state = GameStates.TARGETING

                #message_log.add_message(targeting_item.item.useable.on_use_msg)

            if targeting_cancelled:
                game.state = game.previous_state
                message_log.add_message(Message('Targeting cancelled'))

            if resting:
                visible_enemies = player.visible_enemies(entities, fov_map)
                if len(visible_enemies) > 0:
                    game.state = GameStates.ENEMY_TURN
                else:
                    game.state = GameStates.PLAYER_RESTING

        # Enemies take turns #
        if game.state == GameStates.ENEMY_TURN:
            move_order = sorted(entities, key=lambda i: i.distance_to_ent(player))
            for entity in move_order:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(game, fov_map)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            message = dead_entity.fighter.death(game.map)
                            if dead_entity.is_player:
                                game.state = GameStates.PLAYER_DEAD

                            message_log.add_message(message)

                            if game.state == GameStates.PLAYER_DEAD:
                                break

                    if game.state == GameStates.PLAYER_DEAD:
                        break
            else:
                game.state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    initialize_logging(debugging=True)
    game = initialize_game(debug=False)
    initialize_window(game)
    fov_map = initialize_fov(game.map)
    game_loop(game, fov_map)
