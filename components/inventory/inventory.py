from dataclasses import dataclass, field

from game import GameState
from gui.messages import Message, MessageCategory

@dataclass
class Inventory:
    capacity: int = 0
    items: list = field(default_factory=list)

    def __iter__(self):
        yield from self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, item):
        return self.items[item]

    def __contains__(self, item):
        return item in self.items

    @property
    def is_empty(self):
        return len(self) == 0

    @property
    def is_full(self):
        return len(self) >= self.capacity

    @property
    def useable_items(self):
        return [item_e for item_e in self.items if item_e.item.useable is not None]

    def add(self, item):
        results = []

        if self.is_full:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full.', category=MessageCategory.OBSERVATION)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message(f'You pick up the %{item.color}%{item.name}%%.', category=MessageCategory.OBSERVATION)
            })
            self.items.append(item)

        return results

    def use(self, item_entity, game, **kwargs):
        results = []

        useable = item_entity.item.useable
        item_use_results = useable.use(self.owner, game, **kwargs)

        for item_use_result in item_use_results:
            if item_use_result.get('consumed'):
                self.remove(item_entity)

        results.extend(item_use_results)

        return results

    def drop(self, item):
        results = []

        item.x, item.y = self.owner.x, self.owner.y

        if item in self.owner.paperdoll.equipped_items:
            self.owner.paperdoll.dequip(item)

        self.remove(item)
        results.append({'item_dropped': item, 'message': Message(f'You dropped the {item.name}.')})

        return results

    def prepare(self, item):
        results = []
        inventory = self.owner.inventory
        qu_inventory = self.owner.qu_inventory

        if item in qu_inventory.items and not inventory.is_full:
            qu_inventory.remove(item)
            inventory.add(item)
            results.append({
            'item_prepared': item,
            'message': Message(f'You de-prepare the {item.name}.')})

        elif len(qu_inventory) >= qu_inventory.capacity:
            results.append({
                'message': Message('You cannot prepare any more items.', category=MessageCategory.OBSERVATION)
            })
        else:
            qu_inventory.add(item)
            inventory.remove(item)
            results.append({
                'item_prepared': item,
                'message': Message(f'You prepare the {item.name}.')})

        return results

    def remove(self, item):
        """ removes an item from the player main inventory """
        if item in self.items:
            self.items.remove(item)