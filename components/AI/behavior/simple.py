class Simple:
    """
    Simple behavior moves the npc straight towards the player, attack if next to them and use a skill if available.
    """

    def decide_move(self, target, game):
        npc = self.owner.owner

        results = []

        npc.move_astar(target, game)

        return results
    
    def decide_attack(self, target, game):
        npc = self.owner.owner

        results = []

        attack_results = npc.fighter.attack_setup(target, game)
        results.extend(attack_results)

        return results