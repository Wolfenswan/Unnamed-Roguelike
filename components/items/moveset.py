from random import choice, randint
from typing import List

from map.directions_util import relative_dir, RelativeDirection


class Moveset():
    def __init__(self, movelist):
        self.random = False
        self.movelist = movelist
        self.current_move = 1

        if self.movelist.get('verbs'):
            self.general_verbs = self.movelist['verbs']
            del self.movelist['verbs']

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
        t = '%orange%X%%'
        l_1 = [' ',' ',' ']
        l_2 = [' ','@','%red%X%%']
        l_3 = [' ',' ',' ']
        for extra_attack in self.movelist[self.current_move].get('extend_attack', []):
            if extra_attack == RelativeDirection.BEHIND:
                l_2[2] = t
            if extra_attack == RelativeDirection.LEFT:
                l_1[2] = t
            if extra_attack == RelativeDirection.RIGHT:
                l_3[2] = t
            if extra_attack == RelativeDirection.LEFT_BACK:
                l_1[1] = t
            if extra_attack == RelativeDirection.RIGHT_BACK:
                l_1[3] = t

        return (l_1,l_2,l_3)

    def execute(self, attacker, target):
        move = self.movelist[self.current_move]
        if move.get('extend_attack'):
            move['extra_attacks'] = self.get_extra_attack_positions(attacker, target, move['extend_attack'])
        if move.get('verb') is None:
            move['attack_verb'] = choice(self.general_verbs)
        else:
            move['attack_verb'] = move['verb']
        return move

    def cycle_moves(self, reset=False):
        if self.random:
            self.current_move = randint(1, self.moves)
        else:
            self.current_move += 1

        if self.current_move > self.moves or reset:
            self.current_move = 1

    @staticmethod
    def get_extra_attack_positions(attacker, target, extra_hits:List):
        extra_attacks = []
        x, y = target.pos
        dir = attacker.direction_to_ent(target)

        for extra_hit in extra_hits:
            rel_dir = relative_dir(dir, extra_hit)
            pos = (attacker.x + rel_dir[0], attacker.y + rel_dir[1])
            extra_attacks.append(pos)

        return extra_attacks