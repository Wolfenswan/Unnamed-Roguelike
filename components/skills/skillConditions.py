from gameobjects.util_functions import free_line_between_pos


class SkillCondition:
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
        free_line_between_pos(*actor.pos, *target.pos, game)

    @staticmethod
    def distance_to(**kwargs):
        actor = kwargs.get('actor')
        target = kwargs.get('target')
        min, max = kwargs['min_dist'], kwargs['max_dist']
        if min <= actor.distance_to_ent(target) <= max:
            return True
        else:
            return False

    @staticmethod
    def actor_state(**kwargs):
        """
        Checks whether own state is in a given condition
        Required kwargs: 'state', 'condition'
        """
        actor = kwargs.get('actor')
        state = kwargs['state']
        condition = kwargs['state_condition']

        return actor.effects[state] == condition

    @staticmethod
    def target_state(**kwargs):
        """
        Checks whether target's state is in a given condition
        Required kwargs: 'state', 'condition'
        """
        target = kwargs.get('target')
        state = kwargs['state']
        condition = kwargs['state_condition']

        return target.effects[state] == condition

    @staticmethod
    def always_available():
        return True