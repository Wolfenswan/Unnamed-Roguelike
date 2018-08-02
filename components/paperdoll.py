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
            print(self.equipped_items)
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

    # def equip_old(self, item):
    #     """ this sets the slot to the new item and adds the item to the equipped_items list """
    #     results = []
    #     logging.debug('{0} is equipping {1}'.format(self.owner.name,item.name))
    #
    #     extremity = getattr(self, item.e_to)
    #     slot = getattr(extremity, item.e_type)
    #
    #     # if the slot is already occupied, prompt the player if he wants to remove the other item
    #     if slot:
    #         results.append({'message':Message(f'{slot.name} is already equipped.')})
    #
    #         choice = menu_popup_yesno('', 'Remove your old {0}?'.format(slot.name), center_on_player=True,
    #                                   force_width=24)
    #         if choice:
    #
    #             # if both items have a quick use inventory try swapping their inventories
    #             if hasattr(slot, 'qu_inventory') and hasattr(item, 'qu_inventory'):
    #                 slot.qu_inventory.swap_qu_inv(item.qu_inventory)
    #
    #             slot.dequip(self.owner)
    #             self.equip(item)
    #             Message('You remove your old {0}.'.format(slot.name))
    #             return True
    #         else:
    #             return False
    #     else:
    #         setattr(extremity, item.e_type, item)
    #         self.equipped_items.append(item)
    #         return True


    def get_total_qu_slots(self):
        # TODO should be a @property #
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
