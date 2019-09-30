from debug.timer import debug_timer
from game import GameState
from gameobjects.block_level import BlockLevel
from gui.messages import Message

@debug_timer
def process_turn_results(player_turn_results, game, fov_map):
    player = game.player
    entities = game.entities

    results = {}

    for player_turn_result in player_turn_results:
        message = player_turn_result.get('message')
        fov_recompute = player_turn_result.get('fov_recompute')
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
        level_change = player_turn_result.get('level_change')

        # spawn menu #
        spawn_menu_selection = player_turn_result.get('spawn_menu_selection')

        # List of results that activate the enemy's turn #
        enemy_turn_on = [item_added, item_dropped, item_consumed, item_equipped, item_dequipped, item_prepared, weapon_switched, ranged_attack, waiting]

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
            game.toggle_cursor(pos, state= GameState.CURSOR_TARGETING)
            results['targeting_item']= targeting

        if targeting_cancelled:
            game.state = GameState.PLAYERS_TURN
            Message('Targeting cancelled.').add_to_log(game) # TODO Placeholder

        if waiting:
            # TODO move regeneration into its own function
            if player.in_combat(game):
                if player.f.active_weapon:
                    player.f.active_weapon.moveset.cycle_moves(reset=True) # Waiting resets weapon moves
                if not player.f.sta_full:
                    player.f.recover(player.f.max_stamina / 20)
            else:
                # TODO placeholder values for regeneration/resting
                # if not player.f.hp_full:
                #     player.f.heal(player.f.max_hp/10)
                if not player.f.sta_full:
                    player.f.recover(player.f.max_stamina / 10)

        if door_entity is not None:
            # If the player interacted with a door, update the fov map
            fov_map.transparent[door_entity.y, door_entity.x] = not door_entity.blocks.get(BlockLevel.SIGHT, False)
            fov_map.walkable[door_entity.y, door_entity.x] = not door_entity.blocks.get(BlockLevel.WALK, False)

        if dead_entity is not None:
            dead_entity.f.death(game).add_to_log(game)
            if dead_entity.is_player:
                game.state = GameState.PLAYER_DEAD

        if spawn_menu_selection is not None:
            game.toggle_cursor((player.x+1,player.y), state=GameState.CURSOR_ACTIVE)
            results['debug_spawn']= spawn_menu_selection

        if fov_recompute:
            results['fov_recompute']= fov_recompute

        # Enable enemy turn if at least one of the results is not None
        filtered_enemy_turn_conditions = list(filter(lambda x: x is not None, enemy_turn_on))
        if len(filtered_enemy_turn_conditions) > 0:
            game.state = GameState.NPC_TURN

        if level_change is not None:
            # if level_change > 0 and player.same_pos_as(game.stairs_down) or \
            #         level_change < 0 and player.same_pos_as(game.stairs_up):
            results['level_change'] = level_change
            results['fov_reset'] = True

    return results