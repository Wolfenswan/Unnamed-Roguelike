from data.data_processing import ITEM_DATA, NPC_DATA, ARCHITECTURE_DATA, UNIQUE_DATA
from gui.menus import generic_options_menu


def spawn_menu(game):
    results = []
    npc_data = NPC_DATA
    options = ['NPC', 'Item', 'Object', 'Unique']
    choice = generic_options_menu('Spawn Menu', 'Select Category:',
                                  options, game, sort_by=1,
                                  cancel_with_escape=True)
    if choice == 0:
        # TODO make bodytype selectable
        options = list(npc_data.keys())
        choice= generic_options_menu('Monster Spawning', 'Pick the monster to spawn. Enter to spawn, ESC to cancel.', options, game)
        if choice is not None:
            key = options[choice]
            results.append({'spawn_menu_selection':key})
    elif choice == 1:
        # TODO paginate when items > 26 (or less)
        # TODO make material etc. selectable
        # TODO split between useable & equipment? split by itemType? (submenus?)
        options = list(ITEM_DATA.keys())
        choice = generic_options_menu('Item Spawning',
                              'Pick the item to spawn. Enter to spawn, ESC to cancel.',
                                      options, game)
        if choice is not None:
            key = options[choice]
            results.append({'spawn_menu_selection': key})
    elif choice == 2:
        options = list(ARCHITECTURE_DATA.keys())
        choice = generic_options_menu('Architecture Spawning',
                              'Pick the item to spawn. Enter to spawn, ESC to cancel.',
                                      options, game)
        if choice is not None:
            key = options[choice]
            results.append({'spawn_menu_selection': key})
    elif choice == 3:
        options = list(UNIQUE_DATA.keys())
        choice = generic_options_menu('Unique Spawning',
                              'Pick the item to spawn. Enter to spawn, ESC to cancel.',
                                      options, game)
        if choice is not None:
            key = options[choice]
            results.append({'spawn_menu_selection': key})

    return results