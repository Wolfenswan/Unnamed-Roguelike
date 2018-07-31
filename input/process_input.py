""" Processes the actions from handle_keys into game-events """
import tcod

from game import GameStates
from gameobjects.entity import get_blocking_entities_at_location
from gui.messages import Message, MessageType


def process_input(action, mouse_action, fov_map, game, targeting_item = None):
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
    inventory_index = action.get('inventory_index')
    left_click = mouse_action.get('left_click')
    right_click = mouse_action.get('right_click')

    player_turn_results = []

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
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game.state = GameStates.ENEMY_TURN

        elif rest:
            # player_turn_results.append({'message': Message(f'You wait.'), 'resting': True})
            player_turn_results.append({'resting': True})

        elif pickup:
            for entity in entities:
                if entity.item and entity.same_pos_as(player):
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

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
        game.previous_state = game.state
        game.state = GameStates.DROP_INVENTORY

    # Item usage #
    if inventory_index is not None and game.previous_state != GameStates.PLAYER_DEAD and inventory_index <= len(
            player.inventory.items):
        item = player.inventory.items[inventory_index]

        if game.state == GameStates.SHOW_INVENTORY:
            inv_use_result = player.inventory.use(item, entities=entities, fov_map=fov_map)
            player_turn_results.extend(inv_use_result)
            #     if game.state == GameStates.SHOW_INVENTORY:
            # header = 'Press the key next to an item to use it, or Esc to cancel.\n'
            # inventory_menu('Inventory', header, game)
        elif game.state == GameStates.DROP_INVENTORY:
            player_turn_results.extend(player.inventory.drop_item(item))

    # Targeting #
    # TODO broken at the moment - replace with keyboard controlled cursor
    if game.state == GameStates.TARGETING:
        if left_click:
            target_x, target_y = left_click
            item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                    target_x=target_x, target_y=target_y)
            player_turn_results.extend(item_use_results)
        elif right_click:
            player_turn_results.append({'targeting_cancelled': True})

    if exit:
        if game.state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
            game.state = game.previous_state
        elif game.state == GameStates.TARGETING:
            player_turn_results.append({'targeting_cancelled': True})
        else:
            return True

    if fullscreen:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    return player_turn_results