import logging

import tcod

from config_files import cfg
from game import GameStates, Game
from gui.menus import options_menu
from loader_functions.data_loader import load_game
from turn_processing.handle_input import handle_keys
from turn_processing.process_npc_actions import process_npc_actions
from turn_processing.process_player_actions import process_player_input
from loader_functions.initialize_game import initialize_game
from debug import initialize_logging
from loader_functions.initialize_window import initialize_window
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import render_all
from turn_processing.process_turn_results import process_turn_results


def game_loop(game):
    player = game.player
    entities = game.entities
    fov_map = game.fov_map

    game.state = GameStates.PLAYERS_TURN
    game.previous_state = game.state

    targeting_item = None

    fov_recompute = True

    key = tcod.Key()
    # mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        # tcod.sys_set_fps(30)
        # tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, '')

        logging.debug(f'Beginning turn {game.turn}. State: {game.state}. Recomputing FOV: {fov_recompute}')

        if fov_recompute:
            recompute_fov(game, player.x, player.y)
            fov_recompute = False
        render_all(game, fov_map, debug=game.debug['map'])

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, None, True)
        action = handle_keys(key, game.state)
        #mouse_action = handle_mouse(mouse)

        # Process player input into turn results #
        player_turn_results = process_player_input(action, game, fov_map, targeting_item = targeting_item)
        logging.debug(f'Turn {game.turn} player results: {player_turn_results}')

        # The game exits if player turn results returns False #
        if player_turn_results == False:
            return True

        # Process turn results #
        processed_turn_results = process_turn_results(player_turn_results, game, fov_map)
        logging.debug(f'Turn {game.turn}. State: {game.state}. Processed results: {player_turn_results}')

        # Enemies take turns #
        if game.state == GameStates.ENEMY_TURN:
            process_npc_actions(game)
            game.turn += 1

        # Prepare for next turn #
        for turn_result in processed_turn_results:
            fov_recompute = turn_result.get('fov_recompute', False)
            targeting_item = turn_result.get('targeting_item')

if __name__ == '__main__':
    initialize_logging(debugging=True)
    game = Game(debug=False)
    initialize_window(game)

    choice = options_menu(cfg.GAME_NAME, 'Welcome to the Dungeon', options=['Play a new game', 'Continue last game', 'Quit'], cancel_with_escape=False, sort_by=1)
    if choice == 0:
        game = initialize_game(game)
    elif choice == 1:
        try:
            game = load_game()
        except:
            # TODO show a file loading error popup
            pass
    elif choice == 2:
        exit()

    game.fov_map = initialize_fov(game)

    game_loop(game)

