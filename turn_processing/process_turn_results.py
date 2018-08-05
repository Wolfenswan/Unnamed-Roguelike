import tcod

from game import GameStates
from gui.messages import Message


def process_turn_results(player_turn_results, game, fov_map):
    player = game.player
    message_log = game.message_log
    entities = game.entities

    results = []

    for player_turn_result in player_turn_results:
        fov_recompute = player_turn_result.get('fov_recompute')
        message = player_turn_result.get('message')
        item_added = player_turn_result.get('item_added')
        item_consumed = player_turn_result.get('consumed')
        item_dropped = player_turn_result.get('item_dropped')
        item_equipped = player_turn_result.get('item_equipped')
        item_dequipped = player_turn_result.get('item_dequipped')
        targeting_item = player_turn_result.get('targeting')
        targeting_cancelled = player_turn_result.get('targeting_cancelled')
        waiting = player_turn_result.get('waiting')
        door_entity = player_turn_result.get('door_toggled')
        dead_entity = player_turn_result.get('dead')

        # List of results that activate the enemy's turn #
        enemy_turn_on = [item_added, item_dropped, item_consumed, item_equipped, item_dequipped]

        if message:
            message_log.add_message(message)

        if dead_entity:
            message = dead_entity.fighter.death(game)
            if dead_entity.is_player:
                game.state = GameStates.PLAYER_DEAD
            message_log.add_message(message)

        if item_added:
            entities.remove(item_added)

        if item_dropped:
            entities.append(item_dropped)

        # Enable enemy turn if at least one of the results is valid
        filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
        if len(filtered_enemy_turn_conditions) > 0:
            game.state = GameStates.ENEMY_TURN

        if targeting_item:
            game.previous_state = GameStates.PLAYERS_TURN
            game.state = GameStates.CURSOR_ACTIVE
            game.cursor.x, game.cursor.y = game.player.x, game.player.y
            results.append({'targeting_item': targeting_item})

        if targeting_cancelled:
            game.state = game.previous_state
            message_log.add_message(Message('Targeting cancelled'))

        if waiting:
            visible_enemies = player.visible_enemies(entities, fov_map)
            if len(visible_enemies) > 0:
                player.fighter.toggle_blocking()
                #player.turnplan.plan_turn(game.turn+1, {'planned_function': player.fighter.toggle_blocking})
                game.state = GameStates.ENEMY_TURN
            else:
                game.state = GameStates.PLAYER_RESTING

        if fov_recompute:
            results.append({'fov_recompute': fov_recompute})

        if door_entity:
            tcod.map_set_properties(fov_map, door_entity.x, door_entity.y, not door_entity.blocks_sight, not door_entity.blocks)

    return results