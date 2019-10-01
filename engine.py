import logging

import tcod
import tcod.event

from config_files import cfg
from game import GameState, Game
from gui.menus import main_menu
from loader_functions.data_loader import load_game
from loader_functions.initialize_font import initialize_font
from loader_functions.initialize_game import initialize_game, initialize_map, initialize_objects, initialize_level
from loader_functions.intro import play_intro
from turn_processing.input_handling.handle_keys import handle_keys, handle_keys_legacy
from turn_processing.process_npc_actions import process_npc_actions
from turn_processing.process_player_actions import process_player_input
from debug.logger import initialize_logging
from loader_functions.initialize_window import initialize_window
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import render_all
from turn_processing.process_turn_results import process_turn_results


def game_loop(game):
    player = game.player

    targeting_item = None
    debug_spawn = None
    fov_reset = False
    fov_recompute = True
    new_turn = True
    final_turn_results = {}

    key = tcod.Key()
    # mouse = tcod.Mouse()

    game.fov_map = initialize_fov(game)
    recompute_fov(game, player.x, player.y)
    render_all(game, game.fov_map, debug=game.debug['reveal_map'])

    if game.turn == 1 and not game.debug['no_intro']:
        play_intro(game)

    game.state = GameState.PLAYER_ACTIVE
    game.previous_state = game.state

    while not tcod.console_is_window_closed():
        # tcod.sys_set_fps(30)
        # tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, '')

        if fov_reset:
            game.fov_map = initialize_fov(game)
        if fov_recompute or fov_reset:
            recompute_fov(game, player.x, player.y)
            fov_recompute = False
        render_all(game, game.fov_map, debug=game.debug['reveal_map'])

        if new_turn:
            game.turn += 1
            for ent in game.entities:
                ent.proc_every_turn(game, start=True)
            new_turn = False

        # TODO new tcod.event system
        # action = False
        # for event in tcod.event.wait():
        #     if event.type == "QUIT":
        #         exit()
        #     elif event.type == "KEYDOWN":
        #         action = handle_keys(event, game.state)

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS, key, None, True)
        action = handle_keys_legacy(key, game.state)
        # mouse_action = handle_mouse(mouse)

        if action:
            logging.debug(f'Processing {action}, last turn results: {final_turn_results}')
            # Process player input into turn results #
            # TODO game state should be set in engine.py, not inside the lower functions
            player_turn_results = process_player_input(action, game, last_turn_results=final_turn_results)
            logging.debug(f'Loop starts with turn {game.turn}, player results: {player_turn_results}')
            # The game exits if player turn results returns False #
            if player_turn_results is False:
                break

            # Process turn results #
            # TODO game state should be set in engine.py, not inside the lower functions
            processed_turn_results = process_turn_results(player_turn_results, game, game.fov_map)
            logging.debug(f'Turn {game.turn}. State: {game.state}. Processed results: {player_turn_results}')
            fov_recompute = processed_turn_results.get('fov_recompute', False)
            fov_reset = processed_turn_results.get('fov_reset', False)
            level_change = processed_turn_results.get('level_change')
            if targeting_item is None:
                targeting_item = processed_turn_results.get('targeting_item')
            if debug_spawn is None:
                debug_spawn = processed_turn_results.get('debug_spawn')

            # NPCs take turns #
            if game.npc_active:
                new_turn = True
                for ent in game.entities:
                    ent.proc_every_turn(game, start=False)
                game.state = process_npc_actions(game) # set game state to either player turn or player dead

            # Level Change #
            if level_change is not None and game.player_active:  # player_active prevents level_change if player was killed while trying to change the level
                initialize_level(level_change, game)

            # Resets variables used for targeting/cursor manipulation #
            if game.player_active:
                targeting_item = None
                debug_spawn = None

            final_turn_results = {'targeting_item':targeting_item,'debug_spawn': debug_spawn} # carry over turn results to next loop run

            logging.debug(f'Ending loop at turn {game.turn}. State: {game.state}. FOV Reset/Recompute: {fov_reset}/{fov_recompute}')


if __name__ == '__main__':
    initialize_logging(debugging=cfg.LOGGING['debug'])
    game = Game(debug=cfg.DEBUG)
    initialize_font()
    initialize_window(game)

    while True: # outer loop ensures the game exists to main menu first
        while True:
            start_game = main_menu(game)
            if start_game == 0:
                initialize_game("Player", game)
                # TODO ask for confirmation if savegame exists
                break
            elif start_game == 1:
                try:
                    game = load_game()
                    initialize_window(game) # consoles need to be reinitialized
                    break
                except:
                    # TODO show a file loading error popup
                    exit()
            elif start_game == 3:
                exit()

        game_loop(game)
        game.root.clear() # reset the screen for the main menu

