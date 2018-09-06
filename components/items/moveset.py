import logging


class Moveset():
    def __init__(self, movelist):
        self.movelist = movelist
        self.current_move = 1

    @property
    def moves(self):
        return len(self.movelist.keys())

    def execute(self):
        move = self.movelist[self.current_move]
        self.cycle_moves()
        return move

    def cycle_moves(self, reset=False):
        self.current_move += 1
        if self.current_move > self.moves or reset:
            self.current_move = 1