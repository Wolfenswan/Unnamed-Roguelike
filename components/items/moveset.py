import logging
from random import choice, randint
from typing import List

from data.data_enums import Key, Mod
from map.directions_util import relative_dir, RelativeDirection


class Moveset():
    """
    Moveset is a component for weapon-type equipment. It governs the change of stance
    with each attack, modifying attack values, possible targets and the data to indicate
    these targets in the GUI.
    """
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
    def exert_multipl(self):
        return self.movelist[self.current_move].get(Mod.MOD_MULTIPL, 1)

    @property
    def targets_gui(self):
        """
        The target indicator works by using three lists, each indicating a row in the GUI.
        The 'center' (list 2[1]) represents the player, while the spot to it's 'right' (list 2[2] indicates
        the initially hit target (a red X). All additional targets are drawn as an orange X at their
        respective positions.
        """
        t = '%orange%X%%'
        l_1 = [' ',' ',' ']
        l_2 = [' ','@','%red%X%%',' ']
        l_3 = [' ',' ',' ']
        for extra_attack in self.movelist[self.current_move].get(Key.EXTEND_ATTACK, []):
            if extra_attack == RelativeDirection.BEHIND:
                l_2[3] = t
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

    def modifier(self, modifier_key):
        """ All weapons have various modifiers, with data_keys as names. This function allows to retrieve these values
        by passing a data_key name as argument """
        move = self.movelist[self.current_move]
        mod = self.default_values.get(modifier_key, None)   # Check the moves default values first,
        if mod is None:
            mod = move.get(modifier_key, 1)  # Modifier taken from the move itself
        #logging.debug(f'Moveset({self.owner})-move#{self.current_move}|{modifier_key.name}: {mod}')
        return mod

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