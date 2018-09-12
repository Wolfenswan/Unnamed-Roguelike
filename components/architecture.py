import tcod

from gui.menus import item_list_menu
from gui.messages import Message, MessageCategory


class Architecture:
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    @staticmethod
    def blocks_info(interacting_ent, arch_entity, game):
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
    def toggle_door(interacting_ent, door_ent, game):
        door_ent_closed = door_ent.blocks.get('walk', False)
        results = [{'door_toggled': door_ent, 'fov_recompute': True}]
        # TODO doors can be locked too
        if door_ent_closed:
            door_ent.architecture.on_collision = None
            door_ent.char = '-'
            door_ent.blocks['walk'] = False
            door_ent.blocks['sight'] = False
            door_ent.__descr = 'This door is open.'
            #results.append({'message': Message('You open a door.')})
        else:
            door_ent.architecture.on_collision = Architecture.toggle_door
            door_ent.char = '+'
            door_ent.blocks['walk'] = True
            door_ent.blocks['sight'] = True
            door_ent.__descr = 'This door is closed.'
            #results.append({'message': Message('You close a door.')})

        return results

    @staticmethod
    def open_container(interacting_ent, container_ent, game):
        results = []
        # TODO locks & traps
        # display chest_contents
        if container_ent.inventory.is_empty:
            results.append({'message':Message(f'The {container_ent.name} is empty.', category=MessageCategory.OBSERVATION)})
            # TODO ability to put things into container
        else:
            selection = item_list_menu(container_ent, container_ent.inventory.items, title=f'{container_ent.name}')
            if selection:
                if not interacting_ent.inventory.is_full:
                    results.append({'message':Message(f'You take the {selection.name} from the {container_ent.name}.', category=MessageCategory.OBSERVATION)})
                    container_ent.inventory.remove_from_inv(selection)
                    interacting_ent.inventory.add(selection)
                else:
                    results.append({'message':Message(f'Your inventory is full.', category=MessageCategory.OBSERVATION)})

        if container_ent.inventory.is_empty and container_ent.name[-7:] != '(empty)':
            container_ent.name += ' (empty)'

        return results

    @staticmethod
    def smash_object(interacting_ent, object_ent, game):
        object_ent.char = '%'
        object_ent.color *= 0.3
        object_ent.blocks['walk'] = False
        object_ent.blocks['sight'] = False
        object_ent.architecture = None # TODO not a very elegant solution to prevent rendering in the objects panel
        
        if object_ent.inventory:
            for i in object_ent.inventory.items:
                i.x, i.y = object_ent.x, object_ent.y
                game.entities.append(i)
        
        return [{'message': Message(f'You smash a {object_ent.name.title()}.', category=MessageCategory.OBSERVATION)}]
