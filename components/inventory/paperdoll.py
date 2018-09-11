import logging

from gui.menus import yesno_menu
from gui.messages import Message


class Paperdoll:
    """ The Paperdoll component controls the equipped items of an entity """

    def __init__(self):
        # TODO allow various combination of Heads, Arms etc.
        self.equipped_items = [] # TODO make @property
        self.head = Head()
        self.torso = Torso()
        self.arms = Arms()
        self.legs = Legs()

    def equip(self, item_ent, game):
        results = []
        e_type = item_ent.type.name.lower() # Entity.type is a enum member of the ItemType Class.
        e_to = item_ent.item.equipment.e_to
        qu_slots = item_ent.item.equipment.qu_slots

        extremity = getattr(self, e_to)
        equipped_item = getattr(extremity, e_type)

        print(item_ent.name, extremity, equipped_item)

        if item_ent.item.equipment.two_handed and getattr(self.arms, 'offhand'):
            offhand_item = getattr(self.arms, 'offhand')
            choice = yesno_menu('Remove Offhand Item', f'Remove {offhand_item.name} to equip the two-handed {item_ent.name}?', game)
            if choice:
                results.extend(self.dequip(offhand_item))
            else:
                equipped_item = None
                print('cancelled equipping 2h weapon') # TODO Placeholder

        if equipped_item:
            choice = yesno_menu('Remove Item',f'Unequip your {equipped_item.name}?', game)
            if choice:
                results.extend(self.dequip(equipped_item))
                results.extend(self.equip(item_ent, game))
            else:
                print('kept') # TODO Placeholder

        else:
            setattr(extremity, e_type, item_ent)
            self.equipped_items.append(item_ent)
            self.owner.inventory.remove_from_inv(item_ent)
            if qu_slots:
                self.owner.qu_inventory.capacity += qu_slots

            results.append({'item_equipped': item_ent, 'message': Message(f'You equip the {item_ent.name}')})

        return results

    def dequip(self, item_ent):
        results = []
        e_to = item_ent.item.equipment.e_to
        e_type = item_ent.type.name.lower()
        qu_slots = item_ent.item.equipment.qu_slots

        extremity = getattr(self, e_to)
        equipped_item = getattr(extremity, e_type)

        if equipped_item:
            setattr(extremity, e_type, None)
            self.equipped_items.remove(equipped_item)
            self.owner.inventory.add(equipped_item)
            if qu_slots:
                # TODO make sure items over capacity are moved to regular inventory
                self.owner.qu_inventory.capacity -= qu_slots

            results.append({'item_dequipped': item_ent, 'message': Message(f'You remove the {item_ent.name}')})
        else:
            logging.error('Trying to dequip something that is not equipped. This should not happen...')

        return results

    def is_equipped(self, item):
        return item in self.equipped_items


class Head:
    def __init__(self, armor=None, amulet=None):
        self.armor = armor
        self.amulet = amulet


class Torso:
    def __init__(self, armor=None, shoulder=None, back=None, belt=None):
        self.armor = armor
        self.back = back
        self.shoulder = shoulder
        self.belt = belt


class Arms:
    def __init__(self, armor=None, weapon=None, offhand=None, ring=None):
        self.weapon = weapon
        self.offhand = offhand
        self.armor = armor
        self.ring = ring


class Legs:
    def __init__(self, armor=None, shoes=None):
        self.armor = armor
        self.shoes = shoes
