from game import GameStates
from rendering.common_functions import pos_on_screen
from rendering.draw_windows import draw_options_window

def inventory_menu(game):
    player = game.player
    inventory = player.inventory
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    options = [item.name for item in inventory.items]

    if game.state == GameStates.SHOW_INVENTORY:
        body = 'Press the key next to an item to select it.'
    else:
        body = 'Press the key next to an item to drop it.'

    width = len(max(options, key=len))

    draw_options_window('Inventory', body, options, window_x=x, window_y=y, forced_width=max(width,25))

def item_menu(item_ent, game):
    player = game.player
    x, y = pos_on_screen(player.x + 2, player.y - 2, game.player)

    title = item_ent.name
    body = item_ent.descr

    options = []

    if item_ent.item.useable is not None:
        options.append('(U)se')
    if item_ent.item.equipment is not None:
        options.append('(E)quip')
    options.append('(D)rop')

    draw_options_window(title, body, options, window_x=x, window_y=y, forced_width=len(body), sort_by = None)