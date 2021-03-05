import logging

from data.data_enums import EquipTo
from gui.menus import yesno_menu, item_list_menu
from gui.messages import Message


class Paperdoll:
    """ The Paperdoll component controls the equipped items of an entity """

    # REFACTOR dataclass
    def __init__(self):
        # FUTURE allow various combination of Heads, Arms etc.
        self.weapon_arm = Arm()
        self.shield_arm = Arm()
        self.head = Head()
        self.torso = Torso()
        self.legs = Legs()
        self.owner = None

    @property
    def equipped_items(self):
        items = []
        for attribute, extremity in self.__dict__.items():
            if attribute != 'owner':
                for slot, equipped in extremity.__dict__.items():
                    if equipped is not None:
                        items.append(equipped)
        return items

    @property
    def two_handed_weapons(self):
        """ Returns a list of two-handed weapons the entity is carrying """
        weapons = []
        if self.weapon_arm.carried and self.weapon_arm.carried.item.equipment.two_handed_only:
            weapons.append(self.weapon_arm.carried)
        elif self.weapon_arm.ranged and self.weapon_arm.ranged.item.equipment.two_handed_only:
            weapons.append(self.weapon_arm.ranged)
        return weapons

    def equip(self, item_ent, game=None):
        """
        TODO: refactor so game param is no longer necessary: return conflicting item, let calling function handle menu

        :param item_ent:
        :type item_ent:
        :param game: only required if equip() is allowed to prompt window
        :type game:
        :return:
        :rtype:
        """
        results = []
        e_type = item_ent.type.name.lower() # Entity.type is a enum member of the ItemType Class.

        equip_ent = item_ent.item.equipment
        e_to = equip_ent.e_to
        qu_slots = equip_ent.qu_slots

        extremity = self.get_corresponding_extremity(e_to)
        equipped_item = getattr(extremity, e_type)

        offhand_item = self.shield_arm.carried

        # If new item is two-handed, check if shield arm is occupied #
        if equip_ent.two_handed_only and offhand_item and game is not None:
            choice = yesno_menu('Remove Offhand Item', f'Remove {offhand_item.name_colored} to equip the two-handed {item_ent.name_colored}?', game)
            if choice:
                results.extend(self.dequip(offhand_item))
            else:
                return None

        # If new item is shield, check for two-handed weapons #
        if e_to == EquipTo.SHIELD_ARM and self.two_handed_weapons and game is not None:
            while (len(self.two_handed_weapons) > 0): # loop is required, as both melee and ranged weapon could be two-handed
                choice = item_list_menu(self.owner, self.two_handed_weapons, game,'Remove Two-Handed Weapon', f'Remove which weapon to equip {item_ent.name_colored}?')
                if choice:
                    results.extend(self.dequip(choice))
                else:
                    return None

        # After resolving conflicts for two-handed items, remove items occupying the same slot
        if equipped_item and game is not None:
            choice = yesno_menu('Remove Item',f'Unequip your {equipped_item.name_colored}?', game)
            if choice:
                results.extend(self.dequip(equipped_item))
            else:
                return None

        # After resolving all conflicts, equip new item
        setattr(extremity, e_type, item_ent)
        self.owner.inventory.remove(item_ent)
        if qu_slots:
            self.owner.qu_inventory.capacity += qu_slots

        if self.owner.f.active_weapon is None and e_to == EquipTo.WEAPON_ARM: # If there is no active weapon, set the new weapon as active #
            self.owner.f.active_weapon = item_ent

        results.append({'item_equipped': item_ent, 'message': Message(f'You equip the {item_ent.name_colored}.')})

        return results

    def dequip(self, item_ent):
        results = []
        e_to = item_ent.item.equipment.e_to
        e_type = item_ent.type.name.lower()
        qu_slots = item_ent.item.equipment.qu_slots

        extremity = self.get_corresponding_extremity(e_to)
        equipped_item = getattr(extremity, e_type)

        if equipped_item:
            if qu_slots:
                # TODO make sure items over capacity are moved to regular inventory
                self.owner.qu_inventory.capacity -= qu_slots

            # Disable active weapon if necessary
            if equipped_item == self.owner.f.active_weapon:
                self.owner.f.active_weapon = None

            # Disable blocking if necessary
            if self.owner.f.is_blocking and e_type == 'shield':
                self.owner.f.is_blocking = False

            setattr(extremity, e_type, None)
            self.owner.inventory.add(equipped_item)

            results.append({'item_dequipped': item_ent, 'message': Message(f'You remove the {item_ent.name}.')})
        else:
            logging.error('Trying to dequip something that is not equipped.')

        return results

    def is_equipped(self, item):
        return item in self.equipped_items

    def get_corresponding_extremity(self, enum):
        e_to_str = str(enum.name).lower()  # using the EquipTo Enum name as a string (EquipTo.WEAPON_ARM -> "weapon_arm")
        return getattr(self, e_to_str)  # access the corresponding extremity


class Head:
    def __init__(self, armor=None, weapon=None):
        self.armor = armor
        self.weapon = weapon


class Torso:
    def __init__(self, armor=None, shoulder=None, back=None, belt=None):
        self.armor = armor
        self.back = back
        self.shoulder = shoulder
        self.belt = belt


class Arm:
    def __init__(self, carried=None, wp_ranged=None, armor=None, ring=None):
        self.carried = carried
        self.ranged = wp_ranged
        self.armor = armor
        self.ring = ring

    # Due to the properties and respective setters equipment of various types will only occupy the self.carried slot
    @property
    def melee_weapon(self):
        return self.carried

    @melee_weapon.setter
    def melee_weapon(self, item):
        self.carried = item

    @property
    def shield(self):
        return self.carried

    @shield.setter
    def shield(self, item):
        self.carried = item

    @property
    def misc(self):
        return self.carried

    @misc.setter
    def misc(self, item):
        self.carried = item

    @property
    def ranged_weapon(self):
        return self.ranged

    @ranged_weapon.setter
    def ranged_weapon(self, item):
        self.ranged = item


class Legs:
    def __init__(self, armor=None, shoes=None):
        self.armor = armor
        self.shoes = shoes
