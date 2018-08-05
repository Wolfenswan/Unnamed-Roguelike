import logging

from gui.menus import yesno_menu
from gui.messages import Message


class Paperdoll:
    """ The Paperdoll component controls the equipped items of an entity """

    def __init__(self):
        self.equipped_items = []
        self.head = Head()
        self.torso = Torso()
        self.arms = Arms()
        self.legs = Legs()

    def equip(self, item_ent, game):
        results = []
        e_to = item_ent.item.equipment.e_to
        e_type = item_ent.item.equipment.e_type

        extremity = getattr(self, e_to)
        equipped_item = getattr(extremity, e_type)

        if equipped_item:
            choice = yesno_menu('Remove the item?', game)
            if choice:
                results.extend(self.dequip(equipped_item))
                results.extend(self.equip(item_ent, game))
            else:
                print('kept') # TODO Placeholder
        else:
            setattr(extremity, e_type, item_ent)
            self.equipped_items.append(item_ent)
            self.owner.inventory.remove_from_inv(item_ent)
            results.append({'item_equipped': item_ent, 'message': Message(f'You equip the {item_ent.name}')})

        return results

    def dequip(self, item_ent):
        results = []
        e_to = item_ent.item.equipment.e_to
        e_type = item_ent.item.equipment.e_type

        extremity = getattr(self, e_to)
        equipped_item = getattr(extremity, e_type)

        if equipped_item:
            setattr(extremity, e_type, None)
            self.equipped_items.remove(equipped_item)
            self.owner.inventory.add(equipped_item)
            results.append({'item_dequipped': item_ent, 'message': Message(f'You remove the {item_ent.name}')})
        else:
            logging.error('Trying to dequip something that is not equipped. This should not happen...')

        return results


    def get_total_qu_slots(self):
        """ returns the number of total quick use slots on the paper doll """
        slots = 0
        for i in self.equipped_items:
            slots += getattr(i, 'slots', 0)
        return slots


    def is_equipped(self, item):
        return item in self.equipped_items


class Head:
    def __init__(self, helmet=None, amulet=None):
        self.helmet = helmet
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
        self.rings = ring


class Legs:
    def __init__(self, armor=None, shoes=None):
        self.armor = armor
        self.shoes = shoes
