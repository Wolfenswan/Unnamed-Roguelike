""" Processes the actions from handle_keys into game-events """
import tcod

from game import GameStates
from gameobjects.entity import get_blocking_entities_at_location
from gui.menus import inventory_menu, item_menu, equipment_menu
from gui.messages import Message, MessageType


def process_player_input(action, mouse_action, game, fov_map, targeting_item = None):
    player = game.player
    cursor = game.cursor
    entities = game.entities
    game_map = game.map
    message_log = game.message_log

    exit = action.get('exit')
    fullscreen = action.get('fullscreen')
    move = action.get('move')
    rest = action.get('rest')
    pickup = action.get('pickup')
    show_inventory = action.get('show_inventory')
    show_equipment = action.get('show_equipment')
    # drop_inventory = action.get('drop_inventory')
    # menu_selection = action.get('menu_selection')
    toggle_look = action.get('toggle_look')
    left_click = mouse_action.get('left_click')
    right_click = mouse_action.get('right_click')

    turn_results = []

    # Player moves #
    active_player_states = [GameStates.PLAYERS_TURN, GameStates.PLAYER_RESTING]
    if game.state in active_player_states:
        if move:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    turn_results.append({'fov_recompute':True})

                game.state = GameStates.ENEMY_TURN

        elif rest:
            # turn_results.append({'message': Message(f'You wait.'), 'resting': True})
            turn_results.append({'resting': True})

        elif pickup:
            for entity in entities: # TODO List comprehension can be tested for possible speed gain
                if entity.item and entity.same_pos_as(player):
                    pickup_results = player.inventory.add(entity)
                    turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(
                    Message('There is nothing here to pick up.', msg_type=MessageType.INFO_GENERIC))

    # Cursor Movement & Targeting #
    if toggle_look:
        if game.state == GameStates.CURSOR_ACTIVE:
            game.state = GameStates.PLAYERS_TURN
        else:
            game.state = GameStates.CURSOR_ACTIVE
            game.cursor.x, game.cursor.y = game.player.x, game.player.y

    if game.state == GameStates.CURSOR_ACTIVE:
        if move:
            dx, dy = move
            destination_x = cursor.x + dx
            destination_y = cursor.y + dy
            if tcod.map_is_in_fov(fov_map, destination_x, destination_y):
                cursor.move(dx, dy)

        # if enter is pressed
        # return cursor position for targeting

    # Inventory display #
    if show_inventory:
        if len(player.inventory.items) > 0:
            game.previous_state = game.state
            game.state = GameStates.SHOW_INVENTORY
        else:
            message_log.add_message(Message('Your inventory is empty.'))

    if show_equipment:
        if len(player.paperdoll.equipped_items) > 0:
            game.previous_state = game.state
            game.state = GameStates.SHOW_EQUIPMENT
        else:
            message_log.add_message(Message('You have no items equipped.'))

    # Dropping items #
    # if drop_inventory:
    #     if len(player.inventory.items) > 0:
    #         game.previous_state = game.state
    #         game.state = GameStates.DROP_INVENTORY
    #     else:
    #         message_log.add_message(Message('Your inventory is empty.'))

    # Inventory Interaction #
    selected_item_ent = None

    if game.state == GameStates.SHOW_INVENTORY:
        selected_item_ent = inventory_menu(game)

    elif game.state == GameStates.SHOW_EQUIPMENT:
        selected_item_ent = equipment_menu(game)

    if game.state in [GameStates.SHOW_INVENTORY, GameStates.SHOW_EQUIPMENT]:
        if selected_item_ent:
            item_use_choice = item_menu(selected_item_ent, game)
            if item_use_choice:
                if item_use_choice == 'u':
                    item_interaction_result = player.inventory.use(selected_item_ent, entities=entities, fov_map=fov_map)
                    turn_results.extend(item_interaction_result)
                if item_use_choice == 'e':
                    item_interaction_result = player.paperdoll.equip(selected_item_ent, game)
                    turn_results.extend(item_interaction_result)
                if item_use_choice == 'r':
                    item_interaction_result = player.paperdoll.dequip(selected_item_ent)
                    turn_results.extend(item_interaction_result)
                if item_use_choice == 'd':
                    item_interaction_result = player.inventory.drop(selected_item_ent)
                    turn_results.extend(item_interaction_result)

            else:
                game.state = game.previous_state
        else:
            game.state = game.previous_state

    # if game.state == GameStates.SHOW_ITEM:
    #     if menu_selection is not None and game.previous_state != GameStates.PLAYER_DEAD:
    #         if menu_selection in [ord('e'), ord('E')] and selected_item_ent.item.equipment is not None:
    #             item_interaction_result = player.paperdoll.equip(selected_item_ent, game)
    #             turn_results.extend(item_interaction_result)
    #         if menu_selection in [ord('u'), ord('U')] and selected_item_ent.item.useable is not None:
    #             item_interaction_result = player.inventory.use(selected_item_ent, entities=entities, fov_map=fov_map)
    #             turn_results.extend(item_interaction_result)
    #         if menu_selection in [ord('d'), ord('D')]:
    #             item_interaction_result = player.inventory.drop(selected_item_ent)
    #             turn_results.extend(item_interaction_result)

    # Targeting #
    # TODO broken at the moment - replace with keyboard controlled cursor
    if game.state == GameStates.TARGETING:
        if left_click:
            target_x, target_y = left_click
            item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                    target_x=target_x, target_y=target_y)
            turn_results.extend(item_use_results)
        elif right_click:
            turn_results.append({'targeting_cancelled': True})

    if exit:
        if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            game.state = game.previous_state
        elif game.state == GameStates.TARGETING:
            turn_results.append({'targeting_cancelled': True})
        else:
            return None

    if fullscreen:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    return turn_results