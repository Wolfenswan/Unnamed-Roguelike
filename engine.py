import tcod

from gameobjects.entity import get_blocking_entities_at_location
from game import GameStates
from gui.messages import Message, MessageType
from loader_functions.initialize_game import initialize_game
from loader_functions.initialize_logging import initialize_logging
from rendering.fov_functions import initialize_fov, recompute_fov
from rendering.render_main import clear_all, render_all, pos_on_screen
from loader_functions.initialize_window import initialize_window
from input.handle_input import handle_keys, handle_mouse

def game_loop(game, fov_map):

    player = game.player
    entities = game.entities
    game_map = game.map
    con = game.con
    message_log = game.message_log

    game.state = GameStates.PLAYERS_TURN
    previous_game_state = game.state

    targeting_item = None

    fov_recompute = True

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        #tcod.sys_set_fps(30)
        #tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)

        render_all(game, fov_map, mouse)

        fov_recompute = False

        tcod.console_flush()

        clear_all(con, entities)

        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse, True)

        action = handle_keys(key, game.state)
        mouse_action = handle_mouse(mouse)

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
                player_turn_results.append({'message': Message(f'You wait.'),'resting': True})

            elif pickup:
                for entity in entities:
                    if entity.item and entity.same_pos_as(player):
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)

                        break
                else:
                    message_log.add_message(Message('There is nothing here to pick up.', msg_type=MessageType.INFO_GENERIC))

        # Inventory display #
        if show_inventory:
            if len(player.inventory.items) > 0:
                previous_game_state = game.state
                game.state = GameStates.SHOW_INVENTORY
            else:
                message_log.add_message(Message('Your inventory is empty.'))

        # Dropping items #
        if drop_inventory:
            previous_game_state = game.state
            game.state = GameStates.DROP_INVENTORY

        # Item usage #
        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index <= len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game.state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game.state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

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
                game.state = previous_game_state
            elif game.state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # Results of Player actions #
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            dead_entity = player_turn_result.get('dead')
            targeting_item = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            resting = player_turn_result.get('resting')

            # List of results that activate the enemy's turn #
            enemy_turn_on = [item_added, item_dropped, item_consumed]

            if message:
                message_log.add_message(message)

            if dead_entity:
                message = dead_entity.fighter.death(game.map)
                if dead_entity.is_player:
                    game.state = GameStates.PLAYER_DEAD

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

            if item_dropped:
                entities.append(item_dropped)

            # Enable enemy turn if at least one of the results is valid
            filtered_enemy_turn_conditions = list(filter(lambda x: x != None, enemy_turn_on))
            if len(filtered_enemy_turn_conditions) > 0:
                game.state = GameStates.ENEMY_TURN

            if targeting_item:
                previous_game_state = GameStates.PLAYERS_TURN
                game.state = GameStates.TARGETING

                message_log.add_message(targeting_item.item.on_use_msg)

            if targeting_cancelled:
                game.state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

            if resting:
                nearby_enemies = player.enemies_in_distance(game.entities, dist = player.vision)
                if len(nearby_enemies) > 0:
                    game.state = GameStates.ENEMY_TURN
                else:
                    game.state = GameStates.PLAYER_RESTING

        # Enemies take turns #
        if game.state == GameStates.ENEMY_TURN:
            move_order = sorted(entities, key=lambda i: i.distance_to_ent(player))
            for entity in move_order:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            message = dead_entity.fighter.death(game.map)
                            if dead_entity.is_player:
                                game.state = GameStates.PLAYER_DEAD

                            message_log.add_message(message)

                            if game.state == GameStates.PLAYER_DEAD:
                                break

                    if game.state == GameStates.PLAYER_DEAD:
                        break
            else:
                game.state = GameStates.PLAYERS_TURN

if __name__ == '__main__':
    initialize_logging(debugging=True)
    game = initialize_game(debug=False)
    initialize_window(game)
    fov_map = initialize_fov(game.map)
    game_loop(game, fov_map)