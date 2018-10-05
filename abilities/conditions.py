class AbilityCondition:
    """
    TODO Add:
    Clear line to target
    """

    @staticmethod
    def can_see_target(**kwargs):
        actor = kwargs.get('actor')
        target = kwargs.get('target')
        return actor.distance_to_ent(target) <= actor.fighter.vision

    @staticmethod
    def free_line_to_target(**kwargs):
        actor = kwargs.get('actor')
        target = kwargs.get('target')
        game = kwargs.get('game')
        game.map.free_line_between_tiles(actor.x, actor.y, target.x, target.y)

    @staticmethod
    def distance_to(**kwargs):
        actor = kwargs.get('actor')
        target = kwargs.get('target')
        min, max = kwargs['min_dist'], kwargs['max_dist']
        if min < actor.distance_to_ent(target) < max:
            return True
        else:
            return False

    @staticmethod
    def always_available():
        return True