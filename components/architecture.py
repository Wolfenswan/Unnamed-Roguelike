from gameobjects.block_level import BlockLevel
from gui.menus import item_list_menu
from gui.messages import Message, MessageCategory, MessageType


class Architecture:
    def __init__(self, on_interaction=None, on_collision=None):
        self.on_interaction = on_interaction
        self.on_collision = on_collision

    @staticmethod
    def blocks_info(interacting_ent, arch_entity, game):
        return [{'message': Message(f'{arch_entity.address_colored.title()} blocks your way.', category=MessageCategory.OBSERVATION)}]


    @staticmethod
    def change_level(interacting_ent, arch_entity, game):
        results = []
        if interacting_ent.pos != arch_entity.pos:
            results = [{'message': Message(f'{interacting_ent.address_colored.title()} need to be on top of {arch_entity.address_colored}.', category=MessageCategory.OBSERVATION)}]
        elif arch_entity.char == '<': # up
            results = [{'level_change': -1},]
        elif arch_entity.char == '>': # down
            results = [{'level_change': 1},]
        elif arch_entity.char == '0':
            results =[{'message': Message(f'PLACEHOLDER: You leave the Dungeon.', category=MessageCategory.OBSERVATION, type=MessageType.SYSTEM)}]
        return results


    @staticmethod
    def toggle_door(interacting_ent, door_ent, game):
        door_ent_closed = door_ent.blocks.get(BlockLevel.WALK, False)
        results = [{'door_toggled': door_ent, 'fov_recompute': True}]

        if door_ent_closed: # Open the door
            door_ent.architecture.on_collision = None
            door_ent.char = '-'
            door_ent.blocks[BlockLevel.WALK] = False
            door_ent.blocks[BlockLevel.SIGHT] = False
            door_ent.__descr = 'This door is open.'
            #results.append({'message': Message('You open a door.')})
        else: # Close the door
            door_ent.architecture.on_collision = Architecture.toggle_door
            door_ent.char = '+'
            door_ent.blocks[BlockLevel.WALK] = True
            door_ent.blocks[BlockLevel.SIGHT] = True
            door_ent.__descr = 'This door is closed.'
            #results.append({'message': Message('You close a door.')})

        return results


    @staticmethod
    def open_container(interacting_ent, container_ent, game):
        results = []
        # TODO locks & traps
        # display chest_contents
        if container_ent.inventory.is_empty:
            results.append({'message':Message(f'{container_ent.address_colored.title()} is empty.', category=MessageCategory.OBSERVATION)})
            # TODO ability to put things into container
        else:
            selection = item_list_menu(container_ent, container_ent.inventory, game, title=f'{container_ent.name}')
            if selection:
                if not interacting_ent.inventory.is_full:
                    results.append({'message':Message(f'{interacting_ent.address_colored.title()} take {selection.address_colored} from {container_ent.address_colored}.', category=MessageCategory.OBSERVATION)})
                    container_ent.inventory.remove(selection)
                    interacting_ent.inventory.add(selection)
                else:
                    results.append({'message':Message(f'{interacting_ent.possessive_colored.title()} inventory is full.', category=MessageCategory.OBSERVATION)})

        if container_ent.inventory.is_empty and not '(e)' in container_ent.name:
            container_ent.name += ' (e)'
            container_ent.descr += '\n\nIt is empty.'

        return results


    @staticmethod
    def smash_object(interacting_ent, object_ent, game):
        message = f'{interacting_ent.address_colored.title()} smash {object_ent.address_colored}.'
        object_ent.char = '%'
        object_ent.color *= 0.3
        object_ent.blocks[BlockLevel.WALK] = False
        object_ent.blocks[BlockLevel.SIGHT] = False
        object_ent.architecture = None # TODO not a very elegant solution to prevent rendering in the objects panel
        
        if object_ent.inventory:
            for i in object_ent.inventory:
                i.x, i.y = object_ent.x, object_ent.y
                game.entities.append(i)
        
        return [{'message': Message(message, category=MessageCategory.OBSERVATION)}]
