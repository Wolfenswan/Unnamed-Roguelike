import tcod

from gui.messages import Message, MessageCategory


class Architecture:
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    @staticmethod
    def blocks_info(entity):
        return [{'message': Message(f'A {entity.name} blocks your way.', category=MessageCategory.OBSERVATION)}]

    @staticmethod
    def use_stairs(down):
        if down:
            # generate new dungeon level
            pass
        else:
            # retrieve old dungeon level
            pass

    @staticmethod
    def toggle_door(door_ent):
        door_ent_closed = door_ent.blocks
        results = [{'door_toggled': door_ent, 'fov_recompute': True}]
        # TODO doors can be locked too
        if door_ent_closed:
            door_ent.architecture.on_collision = None
            door_ent.char = '-'
            door_ent.blocks = False
            door_ent.blocks_sight = False
            door_ent.descr = 'This door is open.'
            #results.append({'message': Message('You open a door.')})
        else:
            door_ent.architecture.on_collision = Architecture.toggle_door
            door_ent.char = '+'
            door_ent.blocks = True
            door_ent.blocks_sight = True
            door_ent.descr = 'This door is closed.'
            #results.append({'message': Message('You close a door.')})

        return results

    @staticmethod
    def open_chest(chest_ent):
        # check for trap?
        # display chest_contents
        pass

    @staticmethod
    def smash_object(entity):
        entity.char = '%'
        entity.color *= 0.3
        entity.blocks = False
        entity.blocks_sight = False
        entity.is_corpse = True

        return [{'message': Message(f'You smash a {entity.name.capitalize()}', category=MessageCategory.OBSERVATION)}]
