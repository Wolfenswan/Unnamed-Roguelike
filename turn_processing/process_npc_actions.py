from debug.timer import debug_timer
from game import GameState

@debug_timer
def process_npc_actions(game):
    player = game.player
    move_order = sorted(game.npc_ents, key=lambda i: i.distance_to_ent(game.player))
    for entity in move_order:
        if entity.ai:
            enemy_turn_results = entity.ai.take_turn(game, game.fov_map)
            player.f.surrounded = player.f.check_surrounded(game) # Set the player's surrounded value accordingly

            for enemy_turn_result in enemy_turn_results:
                message = enemy_turn_result.get('message')
                dead_entity = enemy_turn_result.get('dead')

                if message:
                    message.add_to_log(game)

                if dead_entity:
                    dead_entity.f.death(game).add_to_log(game)
                    if dead_entity.is_player and not game.debug['invin']:
                        game.state = GameState.PLAYER_DEAD

                    if game.state == GameState.PLAYER_DEAD:
                        break

            if game.state == GameState.PLAYER_DEAD:
                break
    else:
        game.state = GameState.PLAYERS_TURN