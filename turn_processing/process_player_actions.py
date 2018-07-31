""" Processes the actions from handle_keys into game-events """
import tcod

from game import GameStates
from gameobjects.entity import get_blocking_entities_at_location
from gui.messages import Message, MessageType


def process_player_input(action, mouse_action, game, fov_map, targeting_item = None, selected_item_ent = None):
    player = game.player
    entities = game.entities
    game_map = game.map
    message_log = game.message_log

    exit = action.get('exit')
    fullscreen = action.get('fullscreen')
    move = action.get('move')
    rest = action.get('rest')
    pickup = action.get('pickup')
    show_inventory = action.get('show_inventory')
    drop_inventory = action.get('drop_inventory')
    menu_selection = action.get('menu_selection')
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

    # Inventory display #
    if show_inventory:
        if len(player.inventory.items) > 0:
            game.previous_state = game.state
            game.state = GameStates.SHOW_INVENTORY
        else:
            message_log.add_message(Message('Your inventory is empty.'))

    # Dropping items #
    if drop_inventory:
        if len(player.inventory.items) > 0:
            game.previous_state = game.state
            game.state = GameStates.DROP_INVENTORY
        else:
            message_log.add_message(Message('Your inventory is empty.'))

    # Selecting an item in the inventory #
    if game.state in [GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY] and menu_selection is not None:
        option_index = menu_selection - ord('a')
        if option_index >= 0 and game.previous_state != GameStates.PLAYER_DEAD and option_index <= len(player.inventory.items):
            item = player.inventory.items[option_index]
            if game.state == GameStates.SHOW_INVENTORY:
                turn_results.append({'item_details': item})
            elif game.state == GameStates.DROP_INVENTORY:
                turn_results.extend(player.inventory.drop(item))

    if game.state == GameStates.SHOW_ITEM:
        if menu_selection is not None and game.previous_state != GameStates.PLAYER_DEAD:
            if menu_selection in [ord('e'), ord('E')] and selected_item_ent.item.equipment is not None:
                item_interaction_result = player.inventory.equip(selected_item_ent)
                turn_results.extend(item_interaction_result)
            if menu_selection in [ord('u'), ord('U')] and selected_item_ent.item.useable is not None:
                item_interaction_result = player.inventory.use(selected_item_ent, entities=entities, fov_map=fov_map)
                turn_results.extend(item_interaction_result)
            if menu_selection in [ord('d'), ord('D')]:
                item_interaction_result = player.inventory.drop(selected_item_ent)
                turn_results.extend(item_interaction_result)

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