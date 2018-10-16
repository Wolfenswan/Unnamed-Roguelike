from typing import Optional

from dataclasses import dataclass

from components.items.equipment import Equipment
from components.items.useable import Useable
from data.data_types import Craftsmanship, Condition
from data.gui_data.cond_strings import cond_name_data
from data.gui_data.craft_strings import craft_name_data
from rendering.util_functions import dynamic_wrap

@dataclass
class Item:
    condition: Optional[Condition]
    craftsmanship: Optional[Craftsmanship]
    useable: Optional[Useable]
    equipment: Optional[Equipment]
    identified : bool = False

    def __post_init__(self):
        if self.useable:
            self.useable.owner = self
        if self.equipment:
             self.equipment.owner = self

    def identify(self):
        self.identified = True

    @property
    def prefix(self):
        if self.craftsmanship:
            return craft_name_data.get(self.craftsmanship)

    @property
    def suffix(self):
        if self.condition and self.identified:
            return cond_name_data.get(self.condition)

    @property
    def attr_list(self):
        """
        Returns the item's attributes as formatted string.
        """

        listing = ''
        col = 'desaturated_lime'

        if self.owner.type:
            type_str = self.owner.type.name.title()
            if self.equipment and self.equipment.two_handed:
                type_str += ' (Two-Handed)'
            #list.extend(dynamic_wrap(f' Type: %{col}%{type_str}%%', max_width))
            listing += f'\n\n Type: %{col}%{type_str}%%'

        if self.equipment:

            if self.equipment.e_to:
                e_str = self.equipment.e_to.replace('_',' ')
                #list.extend(dynamic_wrap(f' Equips To: %{col}%{e_str.title()}%%', max_width))
                listing += f'\n\n Equips To: %{col}%{e_str.title()}%%'

            if self.equipment.av:
                 listing += f'\n\n Armor: %{col}%{self.equipment.av}%%'
                # list.extend(dynamic_wrap(f' Armor: %{col}%{self.equipment.av}%%', max_width))
                #list.extend(dynamic_wrap(f' Armor: %{col}%{self.equipment.av}%%', max_width))

            if self.equipment.block_def:
                 listing += f'\n\n Armor (Blocking): %{col}%{self.equipment.block_def}%%'
                # list.extend(dynamic_wrap(f' Armor (Blocking): %{col}%{self.equipment.block_def}%%', max_width))

            if self.equipment.dmg_potential:
                listing += f'\n\n Base Damage: %{col}%{self.equipment.dmg_potential[0]}-{self.equipment.dmg_potential[1]}%%'
                print(listing)
                # list.extend(dynamic_wrap(f' Base Damage: %{col}%{self.equipment.dmg_potential[0]}-{self.equipment.dmg_potential[1]}%%', max_width))

            if self.equipment.attack_range:
                listing += f'\n\n Attack Range: %{col}%{self.equipment.attack_range[0]}-{self.equipment.attack_range[1]}%%'
                print(listing)
                # list.extend(dynamic_wrap(f' Attack Range: %{col}%{self.equipment.attack_range[0]}-{self.equipment.attack_range[1]}%%', max_width))

            if self.equipment.attack_type:
                 listing += f'\n\n Attack: %{col}%{self.equipment.attack_type.name.title()}%%'
                # list.extend(dynamic_wrap(f' Attack: %{col}%{self.equipment.attack_type.name.title()}%%', max_width))

            if self.equipment.l_radius:
                 listing += f'\n\n Light Radius: %{col}%{self.equipment.l_radius}%%'
                # list.extend(dynamic_wrap(f' Light Radius: %{col}%{self.equipment.l_radius}%%', max_width))

            if self.equipment.moveset:
                listing += f'\n\nThis weapon utilizes %orange%{self.equipment.moveset.moves} attacks%%:'
                for k, v in self.equipment.moveset.movelist.items():
                    if v.get('descr'):
                        listing += f'\n%orange%{k}%%: {v.get("descr")}'
                        #list.extend(dynamic_wrap(f'%orange%{k}%%: {v.get("descr")}', max_width))

        return listing