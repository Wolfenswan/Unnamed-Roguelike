from data.data_processing import gen_npc_from_data, NPC_DATA_MERGED, ITEM_DATA_MERGED
from gui.menus import generic_options_menu
from gui.messages import Message, MessageType, MessageCategory


def debug_menu(game):
    results = []
    choice = generic_options_menu('Debug Menu', 'Select Debug Option:',
                                  ['Show full map', 'Invincible Player', 'Entity Debug Information', 'Spawn Monster', 'Spawn Item'], game, sort_by=1,
                                  cancel_with_escape=True)
    if choice == 0:
        game.debug['map'] = not game.debug['map']
        Message(f'Map visibility set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 1:
        game.debug['invin'] = not game.debug['invin']
        Message(f'Player Invincibility set to {game.debug["invin"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 2:
        game.debug['ent_info'] = not game.debug['ent_info']
        Message(f'Entity Debug Information set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 3:
        # TODO make bodytype selectable
        options = list(NPC_DATA_MERGED.keys())
        choice= generic_options_menu('Monster Spawning', 'Pick the monster to spawn. Enter to spawn, ESC to cancel.', options, game)
        if choice is not None:
            key = options[choice]
            results.append({'debug_menu_selection':key})
    elif choice == 4:
        # TODO paginate when items > 26 (or less)
        # TODO make material etc. selectable
        # TODO split between useable & equipment? split by itemType? (submenus?)
        options = list(ITEM_DATA_MERGED.keys())
        choice = generic_options_menu('Item Spawning',
                              'Pick the item to spawn. Enter to spawn, ESC to cancel.',
                                      options, game)
        if choice is not None:
            key = options[choice]
            results.append({'debug_menu_selection': key})

    return results