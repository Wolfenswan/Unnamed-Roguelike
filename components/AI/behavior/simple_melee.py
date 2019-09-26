class Simple:
    """
    Simple behavior moves the npc straight towards the player, attack if next to them and use a skill if available.
    """

    def decide_action(self, target, game):
        actor = self.owner
        distance = actor.distance_to_ent(target)

        results = []

        if distance >= 2:
            actor.move_astar(target, game)
        else:
            results.extend(actor.f.attack_setup(target, game))

        return results