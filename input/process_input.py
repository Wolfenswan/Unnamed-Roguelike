""" Processes the actions from handle_keys into game-events """

import logging

from rendering.menus import menu_popup_inventory, menu_popup_options, menu_itemselection, menu_iteminteraction, \
    menu_popup_quickuse, MenuFilter
from rendering.messages import MessageType, LogLevel, Message

from common import colors, global_vars as gv
from common.game_states import GameStates
from common.helpers import get_monsters, get_items

def process_input(action):
    """ process key input into game actions outside of combat"""

    # TODO: Improve checks by using nearby_monsters()

    logging.debug('Processing action: {0}'.format(action))

    ''' if player is not in combat or the cursor is active '''
    if gv.player.opponent is None or gv.gamestate is GameStates.CURSOR_ACTIVE:

        # moving player outside of combat or moving the cursor
        if 'move' in action:
            x, y = action['move']
            if gv.gamestate == GameStates.CURSOR_ACTIVE:
                gv.cursor.move(x, y)
            elif gv.gamestate == GameStates.PLAYERS_TURN:
                gv.player.move(x, y, gv.player.is_running)
                gv.player.exertion = 0 #TODO DEBUG LINE
                gv.gamestate = GameStates.ENEMY_TURN

        # enabling/disabling running
        elif 'run' == action:
            if gv.player.is_running:
                Message('You stop running.')
                gv.player.is_running = False
            else:
                Message('You start to run.')
                gv.player.is_running = True

        # getting an item from the ground
        elif 'get' == action:
            item = None
            # get all items at the player's feet
            all_items = get_items()
            items = [obj for obj in all_items if [obj.x, obj.y] == [gv.player.x, gv.player.y]]
            if gv.player.inventory.capacity == len(gv.player.inventory.items):
                Message('Your inventory is full, cannot pick up {0}.'.format(item.name))
                item = None
            elif len(items) == 0:
                Message('There is nothing to pick up here!')
            elif len(items) == 1:
                item = 0
            else:
                item = menu_popup_options('', 'What do you want to pick up?', [item.name for item in items],
                                          center_on_player=True, show_cancel_option=True)
            if item is not None:
                items[item].pick_up(gv.player)
                Message('You picked up ' + items[item].name.title() + '!')

        # opening/interacting with the inventory
        elif 'inventory' == action:
            if len(gv.player.inventory.items) == 0:
                Message('Your inventory is empty!')

            # Display the inventory, if it is not already active
            elif gv.gamestate is not GameStates.INVENTORY_ACTIVE:  # if the inventory isn't already active
                gv.gamestate = GameStates.INVENTORY_ACTIVE
                chosen_item = menu_itemselection()  # first, pick an item from the inventory

                while chosen_item is not None:
                    item_action = menu_iteminteraction(chosen_item)  # then decide what to do with it
                    if item_action is None:  # if player cancels, let him/her pick another item (if he cancels here, the entire loop quits)
                        chosen_item = menu_itemselection()
                    elif item_action == 'use':
                        chosen_item.use()
                        gv.gamestate = GameStates.ENEMY_TURN
                        break
                    elif item_action == 'prepare':
                        if chosen_item.prepare(gv.player):
                            Message('You ready the {0} for quick use.'.format(chosen_item.name))
                        else:
                            Message('You don\'t have any free slots!')
                        gv.gamestate = GameStates.ENEMY_TURN
                        break
                    elif item_action == 'drop':
                        chosen_item.drop()
                        Message('You dropped the {0}.'.format(chosen_item.name))
                        gv.gamestate = GameStates.PLAYERS_TURN
                        break
                    elif item_action == 'equip':
                        if chosen_item.equip(gv.player):
                            Message('You equip the {0}.'.format(chosen_item.name))
                        gv.gamestate = GameStates.PLAYERS_TURN
                        break
                if chosen_item is None:  # if inventory interaction was canceled, return to normal
                    gv.gamestate = GameStates.PLAYERS_TURN

        # opening the quick use menu for equipment
        elif 'quickequip' == action:
            if len(gv.player.nearby_monsters(dist=gv.player.get_vision_range())) == 0:
                chosen_item = menu_popup_inventory(caption='Select item to equip:', filter_by=MenuFilter.EQUIPMENT)
                if chosen_item is not None:
                    chosen_item.equip(gv.player)
                    gv.gamestate = GameStates.ENEMY_TURN
                else:
                    gv.gamestate = GameStates.PLAYERS_TURN
            else:
                Message('You can\'t change equipment with monsters nearby!')

        # opening the quick use menu for preparing a usage item
        elif 'quickprepare' == action:
            chosen_item = menu_popup_inventory(caption='Select item to prepare:', filter_by=MenuFilter.USEABLES)
            if chosen_item is not None:
                if chosen_item.prepare(gv.player):
                    Message('You ready the {0} for quick use.'.format(chosen_item.name))
                    gv.gamestate = GameStates.ENEMY_TURN
                else:
                    Message('You don\'t have any free slots!')
                    gv.gamestate = GameStates.PLAYERS_TURN
            else:
                gv.gamestate = GameStates.PLAYERS_TURN

        # opening/interacting with equipped item
        elif 'equipment' == action:
            if len(gv.player.paperdoll.equipped_items) == 0:
                Message('I am naked!')

            elif gv.gamestate is not GameStates.EQUIPMENT_ACTIVE:  # if the inventory isn't already active
                gv.gamestate = GameStates.EQUIPMENT_ACTIVE
                chosen_item = menu_itemselection()  # first, pick an item from the inventory

                while chosen_item is not None:
                    item_action = menu_iteminteraction(chosen_item)  # then decide what to do with it
                    if item_action is None:  # if player cancels, let them pick another item (if they cancel here, the entire loop quits)
                        chosen_item = menu_itemselection()
                    elif item_action == 'remove':
                        if chosen_item.dequip(gv.player):
                            Message('You remove the {0}.'.format(chosen_item.name))
                        gv.gamestate = GameStates.PLAYERS_TURN
                        break
                    elif item_action == 'drop':
                        chosen_item.dequip(gv.player, drop=True)
                        Message('You dropped the {0}.'.format(chosen_item.name))
                        gv.gamestate = GameStates.PLAYERS_TURN
                        break
                if chosen_item is None:  # if inventory interaction was canceled, return to normal
                    gv.gamestate = GameStates.PLAYERS_TURN

        elif 'stairs' == action:
            print(action['stairs'])
            if action['stairs'] == '<' and gv.player.pos() == gv.stairs_down.pos():
                Message('You descend further into the dark abyss.')
                gv.stairs_down.descended = True
            elif action['stairs'] == '>' and gv.player.pos() == gv.stairs_up.pos():
                Message('A heavy trap door has fallen shut on the staircase. You can only go further down.')
            else:
                Message('There are no stairs here.')

    # these actions are always possible, both inside and outside of combat #

    # shifting attention between enemies
    if 'attention' in action and gv.gamestate is GameStates.PLAYERS_TURN:
        dx, dy = action['attention']
        # noinspection PyBroadException
        try:
            monsters = get_monsters()
            monster = next(ent for ent in monsters if (ent.pos()) == (gv.player.x + dx, gv.player.y + dy))
            gv.player.opponent = monster
            Message('You shift attention to the {0}!'.format(monster.name), msg_type=MessageType.INFO_NEUTRAL,
                    log_level=LogLevel.COMBAT)
        except:
            Message('There is nothing there!', log_level=LogLevel.COMBAT)
        gv.gamestate = GameStates.PLAYERS_TURN

    # shifting between nearby targets
    elif 'shift_target' == action: # TODO refactor using yield instead
        monsters = gv.player.nearby_monsters(dist=1.5)
        if len(monsters) >= 1:
            if gv.player.opponent is None:
                gv.player.opponent = monsters[0]
            else:
                i = monsters.index(gv.player.opponent) + 1
                if i >= len(monsters):
                    i = 0
                gv.player.opponent = monsters[i]
            Message('You shift attention to the {0}!'.format(gv.player.opponent.name), msg_type=MessageType.INFO_GENERIC,
                    log_level=LogLevel.COMBAT)
        elif len(monsters) == 0:
            Message('There are no enemies in range.', log_level=LogLevel.GAMEPLAY)
        gv.gamestate = GameStates.PLAYERS_TURN

    # enabling the look cursor
    elif 'look' == action:
        if gv.gamestate == GameStates.CURSOR_ACTIVE:
            Message('You stop looking around.')
            gv.cursor.deactivate()
            gv.gamestate = GameStates.PLAYERS_TURN
        else:
            Message('You start looking around.')
            gv.cursor.activate('*', colors.white)
            gv.gamestate = GameStates.CURSOR_ACTIVE


    # opening the quick use menu
    elif 'quickuse' == action and gv.gamestate is GameStates.PLAYERS_TURN:
        chosen_item = menu_popup_inventory(caption='Select item to use:', filter_by=MenuFilter.QUICKUSE)
        if chosen_item is not None:
            chosen_item.use()
            gv.gamestate = GameStates.ENEMY_TURN
        else:
            gv.gamestate = GameStates.PLAYERS_TURN

    elif 'brandish' == action and gv.gamestate is GameStates.PLAYERS_TURN:
        if gv.player.brandish_weapon():
            Message('You brandish your {0}.'.format(gv.player.get_weapon().name), msg_type=MessageType.INFO_GENERIC)
        else:
            Message('You shake your fists angrily.', msg_type=MessageType.INFO_GENERIC)
        gv.gamestate = GameStates.ENEMY_TURN

    # if player is in combat #
    elif gv.player.opponent and gv.gamestate is GameStates.PLAYERS_TURN:

        opponent = gv.player.opponent

        if 'move' in action:
            dx, dy = action['move']
            if (dx, dy) == (0, 0) or gv.player.direction_to(opponent) == (dx, dy):
                gv.player.move(dx, dy, running=False)
                gv.gamestate = GameStates.ENEMY_TURN
            else:
                Message('You are locked in combat!', log_level=LogLevel.COMBAT)

        elif 'disengage' in action:
            dx, dy = action['disengage']
            result = gv.player.disengage(dx, dy)
            if result is False:  # if the disengagement failed, the enemies will move, otherwise the player gets some time to breathe
                gv.gamestate = GameStates.ENEMY_TURN
        
        elif 'attack_target' == action:
            if opponent:
                gv.player.attack(opponent)
                gv.gamestate = GameStates.ENEMY_TURN
            else:
                Message('You are not targeting anything!')

        else:
            Message('You are locked in combat!', log_level=LogLevel.COMBAT)
