""" Processes the actions from handle_keys into game-events """
import tcod

from game import GameStates
from gameobjects.util_functions import get_blocking_entity_at_location, get_interactable_entity_at_location
from gui.menus import inventory_menu, item_menu, equipment_menu, options_menu
from gui.messages import Message, MessageType
from loader_functions.data_loader import save_game
from rendering.render_windows import render_description_window


def process_player_input(action, game, fov_map, targeting_item = None):
    player = game.player
    cursor = game.cursor
    entities = game.entities
    game_map = game.map
    message_log = game.message_log

    exit = action.get('exit')
    fullscreen = action.get('fullscreen')
    interact = action.get('interact')
    move = action.get('move')
    rest = action.get('rest')
    pickup = action.get('pickup')
    show_inventory = action.get('show_inventory')
    show_equipment = action.get('show_equipment')
    # drop_inventory = action.get('drop_inventory')
    # menu_selection = action.get('menu_selection')
    toggle_look = action.get('toggle_look')
    confirm = action.get('confirm')

    turn_results = []

    # Player moves #
    active_player_states = [GameStates.PLAYERS_TURN, GameStates.PLAYER_RESTING]
    if game.state in active_player_states:
        if move or interact:
            dx, dy = move if move is not None else interact
            destination_x, destination_y = player.x + dx, player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):

                target = get_blocking_entity_at_location(entities, destination_x, destination_y)

                if target is None and interact:
                    target = get_interactable_entity_at_location(entities, destination_x, destination_y)

                if target:
                    # If a NPC is blocking the way #
                    if target.fighter:
                        attack_results = player.fighter.attack(target)
                        turn_results.extend(attack_results)
                    # If a static object is blocking the way #
                    elif target.architecture:

                        if interact and target.architecture.on_interaction: # interacting with the object
                            interaction_results = target.architecture.on_interaction(target)
                            turn_results.extend(interaction_results)

                        if move and target.architecture.on_collision: # bumping into the object
                            collision_results = target.architecture.on_collision(target)
                            turn_results.extend(collision_results)
                    elif move:
                        print('Your way is blocked.') # TODO placeholder
                    elif interact:
                        print('There is nothing to interact with') # TODO placeholder
                elif not interact:
                    player.move(dx, dy)
                    turn_results.append({'fov_recompute':True})

                game.state = GameStates.ENEMY_TURN

        elif rest:
            # turn_results.append({'message': Message(f'You wait.'), 'resting': True})
            turn_results.append({'resting': True})

        elif pickup:
            for entity in entities:  # TODO List comprehension can be tested for possible speed gain
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
            game.previous_state = game.state
            game.state = GameStates.CURSOR_ACTIVE
            cursor.x, cursor.y = game.player.x, game.player.y

    if game.state == GameStates.CURSOR_ACTIVE:
        if move:
            dx, dy = move
            destination_x = cursor.x + dx
            destination_y = cursor.y + dy
            if tcod.map_is_in_fov(fov_map, destination_x, destination_y):
                if targeting_item is None:
                    cursor.move(dx, dy)
                elif player.distance_to_pos(destination_x, destination_y) \
                        < targeting_item.item.useable.function_kwargs['range']:
                    cursor.move(dx, dy)

        if confirm and targeting_item:
            target_x, target_y = cursor.x, cursor.y
            item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                    target_x=target_x, target_y=target_y)
            turn_results.extend(item_use_results)

        if exit and targeting_item:
            turn_results.append({'targeting_cancelled': True})

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

    if exit:
        if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CURSOR_ACTIVE):
            game.state = game.previous_state
        else:
            choice = options_menu('Quit Game', 'Do you want to quit the game?', ['Save & Quit', 'Just Quit'], sort_by=1, cancel_with_escape=True)
            if choice == 0:
                save_game(game)
                return False
            elif choice == 1:
                return False

    if fullscreen:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    return turn_results
