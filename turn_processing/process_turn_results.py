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
        dead_entity = player_turn_result.get('dead')
        item_added = player_turn_result.get('item_added')
        item_consumed = player_turn_result.get('consumed')
        item_dropped = player_turn_result.get('item_dropped')
        item_equipped = player_turn_result.get('item_equipped')
        item_dequipped = player_turn_result.get('item_dequipped')
        item_details = player_turn_result.get('item_details')
        targeting_item = player_turn_result.get('targeting')
        targeting_cancelled = player_turn_result.get('targeting_cancelled')
        resting = player_turn_result.get('resting')

        # List of results that activate the enemy's turn #
        enemy_turn_on = [item_added, item_dropped, item_consumed, item_equipped, item_dequipped]

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

        if item_details:
            game.state = GameStates.SHOW_ITEM
            results.append({'selected_item': item_details})

        # Enable enemy turn if at least one of the results is valid
        filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
        if len(filtered_enemy_turn_conditions) > 0:
            game.state = GameStates.ENEMY_TURN

        if targeting_item:
            game.previous_state = GameStates.PLAYERS_TURN
            game.state = GameStates.TARGETING
            results.append({'targeting_item': targeting_item})

        if targeting_cancelled:
            game.state = game.previous_state
            message_log.add_message(Message('Targeting cancelled'))

        if resting:
            visible_enemies = player.visible_enemies(entities, fov_map)
            if len(visible_enemies) > 0:
                game.state = GameStates.ENEMY_TURN
            else:
                game.state = GameStates.PLAYER_RESTING

        if fov_recompute:
            results.append({'fov_recompute': fov_recompute})

    return results