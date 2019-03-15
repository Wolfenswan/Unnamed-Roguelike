import logging

import tcod

from config_files import cfg
from game import GameState, Game
from gui.menus import generic_options_menu
from loader_functions.data_loader import load_game
from loader_functions.initialize_game import initialize_game
from loader_functions.intro import play_intro
from turn_processing.handle_input import handle_keys
from turn_processing.process_npc_actions import process_npc_actions
from turn_processing.process_player_actions import process_player_input
from debug.logger import initialize_logging
from loader_functions.initialize_window import initialize_window
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import render_all
from turn_processing.process_turn_results import process_turn_results


def game_loop(game):
    player = game.player
    fov_map = game.fov_map

    game.state = GameState.PLAYERS_TURN
    game.previous_state = game.state

    targeting_item = None
    debug_spawn = None
    fov_recompute = True
    final_turn_results = {}

    key = tcod.Key()
    # mouse = tcod.Mouse()

    recompute_fov(game, player.x, player.y)
    render_all(game, game.fov_map, debug=game.debug['map'])

    if game.turn == 1:
        play_intro(game)

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
        # mouse_action = handle_mouse(mouse)

        if action:
            logging.debug(f'Processing {action}')
            # Process player input into turn results #
            player_turn_results = process_player_input(action, game, last_turn_results=final_turn_results)
            logging.debug(f'Turn {game.turn} player results: {player_turn_results}')

            # The game exits if player turn results returns False #
            if player_turn_results is False:
                break

            # Process turn results #
            processed_turn_results = process_turn_results(player_turn_results, game, fov_map)
            logging.debug(f'Turn {game.turn}. State: {game.state}. Processed results: {player_turn_results}')

            # Enemies take turns #
            if game.state == GameState.ENEMY_TURN:

                process_npc_actions(game)

                for ent in game.entities:
                    ent.proc_every_turn(action, game, start=False)
                game.turn += 1
                for ent in game.entities:
                    ent.proc_every_turn(action, game, start=True)

            # Prepare for next turn #
            if processed_turn_results:
                for turn_result in processed_turn_results:
                    fov_recompute = turn_result.get('fov_recompute', False)
                    targeting_item = turn_result.get('targeting_item')
                    debug_spawn = turn_result.get('debug_spawn')
            else:
                fov_recompute = False
                # variables used for cursor-targeting are reset to None, once game state has changed back to the player control
                targeting_item = None if game.state == GameState.PLAYERS_TURN else targeting_item
                debug_spawn = None if game.state == GameState.PLAYERS_TURN else debug_spawn

            final_turn_results = {'targeting_item': targeting_item,
                                  'debug_spawn': debug_spawn}

def main_menu(game_ent):
    choice = generic_options_menu(cfg.GAME_NAME, 'Welcome to the Dungeon',
                                  options=['Play a new game', 'Continue last game', 'Show Options [TBA]', 'Quit'], cancel_with_escape=False,
                                  sort_by=1)
    if choice == 0:
        return initialize_game(game_ent)
    elif choice == 1:
        try:
            return load_game()
        except:
            # TODO show a file loading error popup
            pass
    elif choice == 2:
        # TODO Game Options
        pass
    elif choice == 3:
        return False


if __name__ == '__main__':
    initialize_logging(debugging=True)
    game_ent = Game(debug=False)
    initialize_window(game_ent)

    game = main_menu(game_ent)

    if game is False:
        exit()

    game.fov_map = initialize_fov(game)

    game_loop(game)
