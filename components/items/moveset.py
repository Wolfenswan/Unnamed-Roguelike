import logging


class Moveset():
    def __init__(self, moves):
        self.moves = moves
        self.current_move = 1

    def attack(self, target):
        # get modifiers from current move
        # attack target(s)
        results = self.execute(self.current_move, target)
        self.cycle_moves()
        return results

    def cycle_moves(self, reset=False):
        self.current_move += 1
        if self.current_move > self.moves or reset:
            self.current_move = 1

    def execute(self, *args):
        logging.error(f'Placeholder function was executed by {self}.')

class MovesetSword(Moveset):
    def __init__(self):
        super().__init__(moves = 3)

    def execute(self, move, target):
        results = {}

        if move == 1:
            results['attack_string'] = 'swings at'
        elif move == 2:
            results['attack_string'] = 'slashes'
        elif move == 3:
            results['dmg_mod'] = 0.3
            results['attack_string'] = 'stabs'

        return results

class MovesetSpear(Moveset):
    def __init__(self):
        super().__init__(moves = 3)

    def execute(self, move, target):
        results = {}

        if move == 1:
            results['dmg_mod'] -= 0.2
            results['attack_string'] = 'lightly stabs'
        elif move == 2:
            results['attack_string'] = 'thrusts with accuracy at'
        elif move == 3:
            results['attack_string'] = 'does a powerful thrust through'
            # TODO add enemy behind as extra target

        return results