from debug import debug_timer
from game import GameStates

@debug_timer
def process_npc_actions(game):
    move_order = sorted(game.monster_ents, key=lambda i: i.distance_to_ent(game.player))
    for entity in move_order:
        if entity.ai:
            enemy_turn_results = entity.ai.take_turn(game, game.fov_map)

            for enemy_turn_result in enemy_turn_results:
                message = enemy_turn_result.get('message')
                dead_entity = enemy_turn_result.get('dead')

                if message:
                    message.add_to_log(game)

                if dead_entity:
                    message = dead_entity.fighter.death(game)
                    if dead_entity.is_player:
                        game.state = GameStates.PLAYER_DEAD

                    message.add_to_log(game)

                    if game.state == GameStates.PLAYER_DEAD:
                        break

            if game.state == GameStates.PLAYER_DEAD:
                break
    else:
        game.state = GameStates.PLAYERS_TURN