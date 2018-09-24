import logging


class Actionplan:
    def __init__(self):
        self.planned_queue = []

    def add_to_queue(self, execute_in=1, planned_function=None, planned_function_args=None, fixed=False):
        """
        Add function to queue to execute in n turns.
        # TODO Should instances where an actor has to skip a turn(e.g. stunned) be indicated via a unique switch?

        :param execute_in: Delay until plan is executed.
        :type execute_in: int
        :param planned_function: Planned function to execute
        :type planned_function: function-name
        :param planned_function_args: Arguments to pass on to function
        :type planned_function_args: tuple
        :param fixed: Fixed plans will be overwritten instead of pushed back.
        :type fixed: bool
        """

        logging.debug(f'{self.owner.name} adding to queue ({execute_in, planned_function, planned_function_args, fixed})')

        # Check for any conflicts
        checked_queue = [v for v in self.planned_queue if v['execute_in'] == execute_in]

        if len(checked_queue) > 0:
            # Case 1: Existing plan conflicts and is fixed
            if any(v.get('fixed', False) for v in checked_queue):
                logging.debug(f'Aborting: Conflict with existing & fixed plan(s): {checked_queue}')
            # Case 2: New Plan is fixed
            elif fixed:
                logging.debug(f'Pushing back conflicting plans: {checked_queue}')
                for v in checked_queue:
                    self.add_to_queue(execute_in=v['execute_in']+1, planned_function=v['planned_function'], planned_function_args=v['planned_function_args'], fixed=v['fixed'])

        self.planned_queue.append({
            'execute_in' : execute_in,
            'planned_function': planned_function,
            'planned_function_args': planned_function_args,
            'fixed': fixed
        })

        logging.debug(f'{self.owner.name} Action queue: ({self.planned_queue})')

    def process_queue(self):
        """
        Process the planned queue by reducing the execution delay and execute all actions that have reached a delay of 0.

        :return: Results of executed action(s)
        :rtype: list
        """
        results = []

        for v in self.planned_queue:
            v['execute_in'] -= 1

        execute_plans = [v for v in self.planned_queue if v['execute_in'] == 0]
        if execute_plans:
            for plan in execute_plans:
                logging.debug(f'Executing ({plan}')
                results.extend(self.execute_plan(plan))
                del self.planned_queue[self.planned_queue.index(plan)]

            logging.debug(f'Planned queue after executing plan(s): {self.planned_queue}')

        return results

    @staticmethod
    def execute_plan(plan):
        results = []
        if plan is not None:
            function = plan.get('planned_function')
            function_args = plan.get('planned_function_args')

            if function is None:
                return results

            if function:
                returns = function(*function_args)
                if returns:
                    results.extend(returns)

        return results
