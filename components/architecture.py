import tcod

from gui.menus import inventory_menu
from gui.messages import Message, MessageCategory


class Architecture:
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    @staticmethod
    def blocks_info(*args):
        arch_entity = args[1]
        return [{'message': Message(f'A {arch_entity.name} blocks your way.', category=MessageCategory.OBSERVATION)}]

    @staticmethod
    def use_stairs(down):
        if down:
            # generate new dungeon level
            pass
        else:
            # retrieve old dungeon level
            pass

    @staticmethod
    def toggle_door(*args):
        door_ent = args[1]
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
    def open_container(interacting_ent, container_ent):
        results = []
        # TODO locks & traps
        # display chest_contents
        if container_ent.inventory.is_empty:
            results.append({'message':Message(f'The {container_ent.name} is empty.', category=MessageCategory.OBSERVATION)})
        else:
            selection = inventory_menu(container_ent, title=f'{container_ent.name}')
            if selection:
                if not interacting_ent.inventory.is_full:
                    results.append({'message':Message(f'You take the {selection.name} from the {container_ent.name}.', category=MessageCategory.OBSERVATION)})
                    container_ent.inventory.remove_from_inv(selection)
                    interacting_ent.inventory.add(selection)
                else:
                    results.append({'message':Message(f'Your inventory is full.', category=MessageCategory.OBSERVATION)})

        return results

    @staticmethod
    def smash_object(*args):
        entity = args[1]
        entity.char = '%'
        entity.color *= 0.3
        entity.blocks = False
        entity.blocks_sight = False
        entity.architecture = None # TODO not a very elegant solution to prevent rendering in the objects panel

        return [{'message': Message(f'You smash a {entity.name.capitalize()}', category=MessageCategory.OBSERVATION)}]
