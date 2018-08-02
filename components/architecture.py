import tcod

from gui.messages import Message


class Architecture:
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    def interaction(self):
        pass

    def collision(self):
        pass



    @staticmethod
    def use_stairs(down):
        if down:
            # generate new dungeon level
            pass
        else:
            # retrieve old dungeon level
            pass

    @staticmethod
    def toggle_door(ent):
        door_closed = ent.blocks
        results = [{'door_toggled':ent, 'fov_recompute':True}]
        if door_closed:
            ent.architecture.on_collision = None
            ent.char = '-'
            ent.blocks = False
            ent.blocks_sight = False
            results.append({'message':Message('You open a door.')})
        else:
            ent.architecture.on_collision = toggle_door
            ent.char = '+'
            ent.blocks = True
            ent.blocks_sight = True
            results.append({'message': Message('You close a door.')})

        return results