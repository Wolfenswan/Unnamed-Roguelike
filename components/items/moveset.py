from random import choice, randint
from typing import List

from data.data_keys import Key
from map.directions_util import relative_dir, RelativeDirection


class Moveset():
    def __init__(self, movelist):
        self.random = False
        self.movelist = movelist
        self.current_move = 1

        self.default_values = self.movelist.get(Key.DEFAULT)
        if self.default_values is not None:
            del self.movelist[Key.DEFAULT]
        else:
            self.default_values = {}

    @property
    def moves(self):
        return len(self.movelist.keys())

    @property
    def dmg_multipl(self):
        return self.movelist[self.current_move].get(Key.DMG_MULTIPL, 1)

    @property
    def targets_gui(self):
        t = '%orange%X%%'
        l_1 = [' ',' ',' ']
        l_2 = [' ','@','%red%X%%']
        l_3 = [' ',' ',' ']
        for extra_attack in self.movelist[self.current_move].get(Key.EXTEND_ATTACK, []):
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
        """
        Creates a copy of the current move-dictionary and adds new key/value paris as needed by fighter.attack_setup
        """
        move = self.movelist[self.current_move].copy()
        if move.get(Key.EXTEND_ATTACK):
            move['extra_attacks'] = self.get_extra_attack_positions(attacker, target, move[Key.EXTEND_ATTACK])
        if move.get(Key.VERB) is None:
            move['attack_verb'] = choice(self.default_values[Key.VERBS])
        else:
            move['attack_verb'] = move[Key.VERB]
        return move

    def cycle_moves(self, reset=False):
        if self.default_values.get(Key.RANDOM, False):
            self.current_move = randint(1, self.moves)
        else:
            self.current_move += 1

        if self.current_move > self.moves or reset:
            self.current_move = 1

    @staticmethod
    def get_extra_attack_positions(attacker, target, extra_hits:List):
        """
        Returns all positions (as (x,y) tuples) also affected by the current move.

        :return: [(x1,y1)...(xN,yN)]
        """
        extra_attacks = []
        dir = attacker.direction_to_ent(target)

        for extra_hit in extra_hits:
            rel_dir = relative_dir(dir, extra_hit)
            pos = (attacker.x + rel_dir[0], attacker.y + rel_dir[1])
            extra_attacks.append(pos)

        return extra_attacks