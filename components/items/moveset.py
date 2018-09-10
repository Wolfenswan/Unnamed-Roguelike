import logging


class Moveset():
    def __init__(self, movelist):
        self.movelist = movelist
        self.current_move = 1

    @property
    def moves(self):
        return len(self.movelist.keys())

    def execute(self, attacker, target):
        move = self.movelist[self.current_move]
        if move.get('extra_hits'):
            move['extra_targets'] = self.get_extra_targets(attacker, target, move['extra_hits'])
        self.cycle_moves()
        return move

    def cycle_moves(self, reset=False):
        self.current_move += 1
        if self.current_move > self.moves or reset:
            self.current_move = 1

    @staticmethod
    def get_extra_targets(attacker, target, extra_hits):
        extra_targets = []
        x, y = target.pos
        dir_x, dir_y = attacker.direction_to_ent(target)

        if extra_hits.get('behind_target'):
            target_x = x - dir_x if dir_x > 0 else x + dir_x
            target_y = y - dir_y if dir_y > 0 else y + dir_y
            extra_targets.append((target_x, target_y))

        return extra_targets