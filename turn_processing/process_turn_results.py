import tcod

from game import GameState
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
        weapon_switched = player_turn_result.get('weapon_switched')
        targeting = player_turn_result.get('targeting')
        targeting_cancelled = player_turn_result.get('targeting_cancelled')
        ranged_attack = player_turn_result.get('ranged_attack')
        waiting = player_turn_result.get('waiting')
        door_entity = player_turn_result.get('door_toggled')
        dead_entity = player_turn_result.get('dead')

        # List of results that activate the enemy's turn #
        enemy_turn_on = [item_added, item_dropped, item_consumed, item_equipped, item_dequipped, item_prepared, weapon_switched, ranged_attack]

        if message is not None:
            message.add_to_log(game)

        if weapon_switched is not None:
            Message(f'You ready your %{weapon_switched.color}%{weapon_switched.name}%%.').add_to_log(game)

        if item_added is not None:
            entities.remove(item_added)

        if item_consumed is not None:
            if item_consumed in player.inventory:
                player.inventory.remove(item_consumed)
            if item_consumed in player.qu_inventory:
                player.qu_inventory.remove(item_consumed)

        if item_dropped is not None:
            entities.append(item_dropped)

        if targeting is not None:
            nearest_ent = player.nearest_entity(game.npc_ents, max_dist=targeting.item.useable.on_use_params.get('range',(1,1))[1])
            pos = nearest_ent.pos if nearest_ent is not None else player.pos
            game.toggle_cursor(pos, state=GameState.CURSOR_TARGETING)
            results.append({'targeting_item': targeting})

        if targeting_cancelled is not None:
            game.state = GameState.PLAYERS_TURN
            Message('Targeting cancelled.').add_to_log(game)

        if waiting is not None:
            if player.in_combat(game):
                if player.fighter.active_weapon:
                    player.fighter.active_weapon.moveset.cycle_moves(reset=True) # Waiting resets weapon moves
                game.state = GameState.ENEMY_TURN
            else:
                # TODO placeholder for regeneration/resting
                player.fighter.hp += player.fighter.max_hp/10
                player.fighter.recover(player.fighter.max_stamina / 10) # TODO Placeholder Stamina Managment
                #game.state = GameState.PLAYER_RESTING

        if fov_recompute is not None:
            results.append({'fov_recompute': fov_recompute})

        if door_entity is not None:
            # If the player interacted with a door, the fov map is updated)
            tcod.map_set_properties(fov_map, door_entity.x, door_entity.y, not door_entity.blocks.get(BlockLevel.SIGHT, False), not door_entity.blocks.get(BlockLevel.WALK, False))

        if dead_entity is not None:
            message = dead_entity.fighter.death(game)
            if dead_entity.is_player:
                game.state = GameState.PLAYER_DEAD
            message.add_to_log(game)

        # Enable enemy turn if at least one of the results is not None
        filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
        if len(filtered_enemy_turn_conditions) > 0:
            game.state = GameState.ENEMY_TURN

    return results