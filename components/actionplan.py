import logging
from collections import Callable
from typing import Tuple, Dict


class Actionplan:
    """
    Actionplan govers the AI's skill usage and skill execution in future turns. It contains a queueing-system containing
    skill related functions to be executed in x turns. Whenever a function reaches the queue's first position it is executed, usually
    overriding the AI's regular behavior (moving/attacking etc.) by executing a skill.
    """
    def __init__(self):
        self.planned_queue = []

    def add_to_queue(self, execute_in:int, planned_function:Callable, planned_function_args:Tuple=None, planned_function_kwargs:Dict=None, fixed:bool=False, exclusive:bool=False):
        """
        Add function to queue to execute in n turns.

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
            # Case 1: Existing plan conflicts and is exclusive (TODO NOT FULLY IMPLEMENTED)
            if any(v.get('exclusive', False) for v in checked_queue):
                plan = checked_queue[0]
                logging.debug(f'Conflict with existing & exclusive plan(s): {checked_queue}')
                # If existing plan is also fixed...
                if plan.get('fixed', False):
                    # ... and new plan also fixed, override old fixed plan
                    if fixed:
                        self.planned_queue.remove(checked_queue[0])
                    # ... and new plan is not fixed, add it one spot later
                    else:
                        self.add_to_queue(execute_in+1, planned_function, planned_function_args, planned_function_kwargs, fixed=fixed, exclusive=exclusive)
                        return
                # If existing exclusive plan is not fixed, push it back
                else:
                    self.add_to_queue(plan['execute_in'] + 1, plan['planned_function'],
                                     plan['planned_function_args'], plan['planned_function_kwargs'], fixed=plan['fixed'],
                                      exclusive=plan['exclusive'])

            # Case 2: New plan is exclusive but existing plan at the spots are not, all other plans will have to be pushed back or overwritten
            elif exclusive:
                for plan in checked_queue:
                    if not plan.get('fixed', False): # If the plan is not fixed, it will be pushed back
                        self.add_to_queue(plan['execute_in'] + 1, plan['planned_function'],
                                          plan['planned_function_args'], plan['planned_function_kwargs'], fixed=plan['fixed'], exclusive=plan['exclusive'])
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

        execute_plans = [v for v in self.planned_queue if v['execute_in'] == 0]
        if execute_plans:
            for plan in execute_plans:
                logging.debug(f'Executing ({plan}')
                results.extend(self.execute_plan(plan))
                self.planned_queue.remove(plan)

            logging.debug(f'Planned queue after executing plan(s): {self.planned_queue}')

        for v in self.planned_queue:
            v['execute_in'] -= 1

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
