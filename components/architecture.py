class Architecture():
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    def interaction(self):
        pass

    def collision(self):
        pass

    def toggle_door(self, open):
        if open:
            self.char = '/'
            self.on_interaction = 'self.toggle_door(False)'
            self.on_collision = None
            self.blocks = False

    @staticmethod
    def use_stairs(down):
        if down:
            # generate new dungeon level
            pass
        else:
            # retrieve old dungeon level
            pass
