import tcod

from gui.messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message(f'You pick up the {item.name}!', tcod.blue)
            })

            self.items.append(item)

        return results

    def remove_from_inv(self, item):
        """ removes an item from the player main inventory or any quick use slots """
        if item in self.items:
            self.items.remove(item)

    def is_full(self):
        return True if len(self.items) == self.capacity else False

    def use(self, item_entity, **kwargs):
        results = []

        useable_component = item_entity.item.useable

        if useable_component.use_function is None:
            results.append({'message': Message(f'The {item_entity.name} cannot be used')})
        else:
            if useable_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity,'message': useable_component.on_use_msg})
            else:
                kwargs = {**useable_component.function_kwargs, **kwargs}
                item_use_results = useable_component.use_function(caster = self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        item.x, item.y = self.owner.x, self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message(f'You dropped the {item.name}')})

        return results

    def equip_item(self):
        pass

    def dequip_item(self):
        pass