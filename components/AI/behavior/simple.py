from random import choice


class Simple:
    """
    Simple behavior moves the npc straight towards the player, attack if next to them and use a skill if available.
    """

    def decide_move(self, game):
        target = game.player
        game_map = game.map
        entities = game.entities
        npc = self.owner.owner

        results = []

        npc.move_astar(target, entities, game_map)

        return results
    
    def decide_attack(self, target, game):
        npc = self.owner.owner

        results = []

        attack_results = npc.fighter.attack(target)
        results.extend(attack_results)

        return results