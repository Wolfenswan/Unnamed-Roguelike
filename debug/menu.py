from data.data_processing import gen_npc_from_dict, NPC_DATA_MERGED
from gui.menus import options_menu
from gui.messages import Message, MessageType, MessageCategory


def debug_menu(game):
    results = []
    choice = options_menu('Debug Menu', 'Select Debug Option:',
                          ['Show full map', 'Invincible Player', 'Entity Debug Information', 'Spawn Monster', 'Spawn Item (Not implemented!)'], sort_by=1,
                          cancel_with_escape=True)
    if choice == 0:
        game.debug['map'] = not game.debug['map']
        Message(f'Map visibility set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 1:
        game.debug['invin'] = not game.debug['invin']
        Message(f'Player Invincibility set to {game.debug["invin"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 2:
        game.debug['ent_info'] = not game.debug['ent_info']
        Message(f'Entity Debug Information set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 3: # TODO make bodytype selectable
        options = list(NPC_DATA_MERGED.keys())
        choice= options_menu('Monster Spawning', 'Pick the monster to spawn. The tile to the right of the player must not be blocked.', options)
        if choice is not None:
            key = options[choice]
            #results.append({'debug_spawn':choice})
            if game.map.is_blocked(game.player.x+1, game.player.y, game.blocking_ents):
                Message(f'Position blocked!', type=MessageType.GAME).add_to_log(game)
            else:
                npc = gen_npc_from_dict(NPC_DATA_MERGED[key], game.player.x+1, game.player.y, game)
                game.entities.append(npc)
    elif choice == 4:
        # Select Type, key, material, condition, craft
        pass

    return results