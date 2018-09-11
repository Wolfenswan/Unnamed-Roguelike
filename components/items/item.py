import textwrap

from data.descr_data.craft_descr import craft_name_data
from data.shared_data.types_data import Condition, Craftsmanship


class Item:
    def __init__(self, condition=None, craftsmanship=None, identified=False, useable=None, equipment=None):
        self.condition = condition
        self.craftsmanship = craftsmanship
        self.identified = identified
        self.useable = useable
        self.equipment = equipment

        if self.useable:
            useable.owner = self

        if self.equipment:
            equipment.owner = self

    def identify(self):
        new_name = self.owner.name
        condition = self.condition
        craftsmanship = self.craftsmanship

        if condition == Condition.POOR:
            new_name += ' (-)'
        elif condition == Condition.GOOD:
            new_name += ' (+)'
        elif condition == Condition.LEGENDARY:
            new_name += ' (++)'

        if craftsmanship != Craftsmanship.NORMAL and craftsmanship is not None:
            new_name = f'{craft_name_data[craftsmanship]} {new_name}'

        self.owner.name = new_name.title()
        self.identified = True

    def attr_list(self, max_width=100):
        """
        :return:
        :rtype: list
        """
        list = ['']
        if self.owner.type:
            type_str = self.owner.type.name.capitalize()
            if self.equipment and self.equipment.two_handed:
                type_str += ' (Two-Handed)'
            list.extend(textwrap.wrap(f' Type: {type_str}', max_width))

        if self.equipment:

            if self.equipment.e_to:
                e_str = self.equipment.e_to.replace('_',' ').title()
                list.extend(textwrap.wrap(f' Equips To: {e_str}', max_width))

            if self.equipment.av:
                list.extend(textwrap.wrap(f' Armor: {self.equipment.av}', max_width))

            if self.equipment.dmg_range:
                list.extend(textwrap.wrap(f' Damage Potential: {self.equipment.dmg_range[0]}-{self.equipment.dmg_range[1]}', max_width))

            if self.equipment.l_radius:
                list.extend(textwrap.wrap(f' Light Radius: {self.equipment.l_radius}', max_width))

            if self.equipment.moveset:
                list.append('')
                list.extend(textwrap.wrap(f' This weapon cycles through {self.equipment.moveset.moves} attacks:', max_width))
                for k, v in self.equipment.moveset.movelist.items():
                    list.extend(textwrap.wrap(f'{k}: {v["descr"]}', max_width))

        return list