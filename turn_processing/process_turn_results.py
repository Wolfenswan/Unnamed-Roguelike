import tcod

from game import GameStates
from gameobjects.block_level import BlockLevel
from gui.messages import Message

def process_turn_results(player_turn_results, game, fov_map):
    player = game.player
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
        item_prepared = player_turn_result.get('item_prepared')
        targeting_item = player_turn_result.get('targeting')
        targeting_cancelled = player_turn_result.get('targeting_cancelled')
        waiting = player_turn_result.get('waiting')
        door_entity = player_turn_result.get('door_toggled')
        dead_entity = player_turn_result.get('dead')

        # List of results that activate the enemy's turn #
        enemy_turn_on = [item_added, item_dropped, item_consumed, item_equipped, item_dequipped, item_prepared]

        if message:
            message.add_to_log(game)

        if dead_entity:
            message = dead_entity.fighter.death(game)
            if dead_entity.is_player:
                game.state = GameStates.PLAYER_DEAD
            message.add_to_log(game)

        if item_added:
            entities.remove(item_added)

        if item_dropped:
            entities.append(item_dropped)

        if targeting_item:
            game.previous_state = GameStates.PLAYERS_TURN
            game.state = GameStates.CURSOR_ACTIVE
            game.cursor.x, game.cursor.y = game.player.x, game.player.y
            results.append({'targeting_item': targeting_item})

        if targeting_cancelled:
            game.state = game.previous_state
            Message('Targeting cancelled').add_to_log(game)

        if waiting:
            if player.in_combat(game):
                if player.fighter.weapon:
                    player.fighter.weapon.moveset.cycle_moves(reset=True) # Waiting resets weapon moves
                game.state = GameStates.ENEMY_TURN
            else:
                # TODO placeholder for regeneration/resting
                player.fighter.hp += player.fighter.max_hp/10
                player.fighter.recover(player.fighter.max_stamina / 10) # TODO Placeholder Stamina Managment
                game.state = GameStates.PLAYER_RESTING

        if fov_recompute:
            results.append({'fov_recompute': fov_recompute})

        if door_entity:
            # If the player interacted with a door, the fov map is updated)
            tcod.map_set_properties(fov_map, door_entity.x, door_entity.y, not door_entity.blocks.get(BlockLevel.SIGHT, False), not door_entity.blocks.get(BlockLevel.WALK, False))

        # Enable enemy turn if at least one of the results is valid
        filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
        if len(filtered_enemy_turn_conditions) > 0:
            game.state = GameStates.ENEMY_TURN

    return results