import logging

from gui.messages import Message


# TODO rewrite for new system

class Paperdoll:
    """ The Paperdoll component controls the equipped items of an entity """

    def __init__(self):
        self.owner = None
        self.equipped_items = []
        self.head = Head()
        self.torso = Torso()
        self.arms = Arms()
        self.legs = Legs()

    def equip(self, item):
        """ this sets the slot to the new item and adds the item to the equipped_items list """
        results = []
        logging.debug('{0} is equipping {1}'.format(self.owner.name,item.name))

        extremity = getattr(self, item.e_to)
        slot = getattr(extremity, item.e_type)

        # if the slot is already occupied, prompt the player if he wants to remove the other item
        if slot:
            results.append({'message':Message(f'{slot.name} is already equipped.')})

            choice = menu_popup_yesno('', 'Remove your old {0}?'.format(slot.name), center_on_player=True,
                                      force_width=24)
            if choice:

                # if both items have a quick use inventory try swapping their inventories
                if hasattr(slot, 'qu_inventory') and hasattr(item, 'qu_inventory'):
                    slot.qu_inventory.swap_qu_inv(item.qu_inventory)

                slot.dequip(self.owner)
                self.equip(item)
                Message('You remove your old {0}.'.format(slot.name))
                return True
            else:
                return False
        else:
            setattr(extremity, item.e_type, item)
            self.equipped_items.append(item)
            return True

    def dequip(self, item):
        """ this sets the formerly occupied slot to None and removes the item from the equipped_items list """

        extr = getattr(self, item.e_to)
        slot = getattr(extr, item.e_type)
        if slot:
            setattr(extr, item.e_type, None)
            self.equipped_items.remove(item)
            return True
        else:
            logging.error('Trying to dequip something that is not equipped. This should not happen...')

    def apply_equipment_effects(self):
        pass

    def get_total_qu_slots(self):
        """ returns the number of total quick use slots on the paper doll """
        slots = 0
        for i in self.equipped_items:
            slots += getattr(i, 'slots', 0)
        return slots


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
