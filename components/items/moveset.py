import logging
from random import choice, randint

import tcod


class Moveset():
    def __init__(self, movelist):
        self.random = False
        self.movelist = movelist
        self.current_move = 1

        if self.movelist.get('random'):
            self.random = True
            del self.movelist['random']

    @property
    def moves(self):
        return len(self.movelist.keys())

    @property
    def dmg_multipl(self):
        return self.movelist[self.current_move].get('dmg_multipl', 1)

    @property
    def targets_gui(self):
        l_1 = [' ',' ',' ']
        l_2 = [' ','@','%red%X%']
        l_3 = [' ',' ',' ']
        extra_hits = self.movelist[self.current_move].get('extra_hits', {})
        if extra_hits.get('target_behind'):
            l_2 += '%red%X%'
        if extra_hits.get('target_left'):
            l_1[2] = '%red%X%'
        if extra_hits.get('target_right'):
            l_3[2] = 'X'

        return (l_1,l_2,l_3)

    def execute(self, attacker, target):
        move = self.movelist[self.current_move]
        if move.get('extra_hits'):
            move['extra_targets'] = self.get_extra_targets(attacker, target, move['extra_hits'])
        if not isinstance(move['string'], str):
            move['string'] = choice(move['string'])
        self.cycle_moves()
        return move

    def cycle_moves(self, reset=False):
        if self.random:
            self.current_move = randint(1, self.moves)
        else:
            self.current_move += 1

        if self.current_move > self.moves or reset:
            self.current_move = 1

    @staticmethod
    def get_extra_targets(attacker, target, extra_hits):
        extra_targets = []
        x, y = target.pos
        dir_x, dir_y = attacker.direction_to_ent(target)

        if extra_hits.get('target_behind'):
            target_x = x - dir_x if dir_x > 0 else x + dir_x
            target_y = y - dir_y if dir_y > 0 else y + dir_y
            extra_targets.append((target_x, target_y))

        return extra_targets