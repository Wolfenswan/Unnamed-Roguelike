class Turnplan:
    def __init__(self):
        self.planned_turns = {}

    def execute_plan(self, game_turn):
        results = []
        plan = self.planned_turns.get(game_turn)
        if plan is not None:
            skip_turn = plan.get('skip_turn')
            skill = plan.get('planned_skill')
            skill_args = plan.get('planned_skill_args',())
            function = plan.get('planned_function')
            function_args = plan.get('planned_function_args')

            if skip_turn:
                return results

            if skill:
                results.extend(skill.execute(*skill_args))

            if function:
                results.extend(function(*function_args))

        return results

    def plan_turn(self, turn_to_plan, plan, overwrite=False, pushback=False):
        # If there's already a plan for the intended turn, push that plan back one turn
        if not self.planned_turns.get(turn_to_plan) or overwrite:
            self.planned_turns[turn_to_plan] = plan
        elif pushback: # If there's already a plan for the intended turn, push that plan back one turn TODO needs testing
            self.plan_turn(turn_to_plan + 1, self.planned_turns.get(turn_to_plan), pushback=True)
        else:
            self.planned_turns[turn_to_plan] = self.planned_turns[turn_to_plan] + plan


    def skip_turns(self, num_of_turns, game_turn):
        for i in range(num_of_turns):
            self.plan_turn(game_turn+i+1, {'skip_turn':True}, overwrite=True)
