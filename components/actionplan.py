import logging
from collections import Callable
from typing import Tuple


class Actionplan:
    def __init__(self):
        self.planned_queue = []

    def add_to_queue(self, execute_in:int=1, planned_function:Callable=None, planned_function_args:Tuple=None, fixed:bool=False, exclusive:bool=False):
        """
        Add function to queue to execute in n turns.
        # TODO Should instances where an actor has to skip a turn(e.g. stunned) be indicated via a unique switch?

        :param execute_in: Delay until plan is executed.
        :param planned_function: Planned function to execute
        :param planned_function_args: Arguments to pass on to function
        :param fixed: Fixed plans can not be pushed back by other plans and will be overwritten by ecxlusive plans.
        :param exclusive: Exclusive plans forbid any other plans from happening at the same time.
        """

        logging.debug(f'{self.owner} adding to queue ({execute_in, planned_function, planned_function_args, fixed})')

        # Check if any other plans are set to execute at the same time
        checked_queue = [v for v in self.planned_queue if v['execute_in'] == execute_in]

        if len(checked_queue) > 0:
            # Case 1: Existing plan conflicts and is fixed
            if any(v.get('exclusive', False) for v in checked_queue):
                logging.debug(f'Aborting: Conflict with existing & exclusive plan(s): {checked_queue}')
                # TODO should new plan be added one turn after exclusive plan?
                # TODO what if both are exclusive?
                return
            # Case 2: New plan is exclusive, all other plans will have to be pushed back or overwritten
            elif exclusive:
                for plan in checked_queue:
                    if not plan.get('fixed', False): # If the plan is not fixed, it will be pushed back
                        self.add_to_queue(execute_in=plan['execute_in'] + 1, planned_function=plan['planned_function'],
                                          planned_function_args=plan['planned_function_args'], fixed=plan['fixed'], exclusive=plan['exclusive'])
                    else: # otherwise it will simply be deleted
                        self.planned_queue.remove(plan)

        self.planned_queue.append({
            'execute_in' : execute_in,
            'planned_function': planned_function,
            'planned_function_args': planned_function_args,
            'fixed': fixed,
            'exclusive': exclusive
        })

        logging.debug(f'{self.owner} New Action queue: ({self.planned_queue})')

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
                self.planned_queue.remove(plan)

            logging.debug(f'Planned queue after executing plan(s): {self.planned_queue}')

        return results

    @staticmethod
    def execute_plan(plan):
        results = []
        if plan is not None:
            function = plan.get('planned_function')
            function_args = plan.get('planned_function_args')

            if not isinstance(function_args, tuple):
                function_args = (function_args,)

            if function is None:
                return results

            if function:
                returns = function(*function_args)
                if returns:
                    results.extend(returns)

        return results
