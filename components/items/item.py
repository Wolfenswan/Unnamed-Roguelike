from typing import Optional

from dataclasses import dataclass

from components.items.equipment import Equipment
from components.items.useable import Useable
from data.data_keys import Key
from data.data_types import Craftsmanship, Condition
from data.gui_data.cond_strings import cond_name_data
from data.gui_data.craft_strings import craft_name_data

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
            type_str = self.owner.type.name.replace('_',' ')
            if self.equipment and self.equipment.two_handed:
                type_str += ' (Two-Handed)'
            listing += f'\n\n Type: %{col}%{type_str.title()}%%'

        if self.equipment:
            e_c = self.equipment
            
            if e_c.e_to:
                e_str = e_c.e_to.replace('_',' ')
                listing += f'\n\n Equips To: %{col}%{e_str.title()}%%'

            if e_c.av:
                 listing += f'\n\n Armor: %{col}%{e_c.av}%%'

            if e_c.block_def:
                 listing += f'\n\n Armor (Blocking): %{col}%{e_c.block_def}%%'

            if e_c.dmg_potential:
                listing += f'\n\n Base Damage: %{col}%{e_c.dmg_potential[0]}-{e_c.dmg_potential[1]}%%'

            if e_c.attack_range:
                listing += f'\n\n Attack Range: %{col}%{e_c.attack_range[0]}-{e_c.attack_range[1]}%%'

            if e_c.l_radius:
                 listing += f'\n\n Light Radius: %{col}%{e_c.l_radius}%%'

            if e_c.moveset:
                listing += f'\n\nThis weapon utilizes %orange%{e_c.moveset.moves} attacks%%:'
                for k, v in e_c.moveset.movelist.items():
                    if v.get(Key.DESCR) is not None:
                        listing += f'\n%orange%({k})%% {v.get(Key.DESCR)}'

        if self.useable:
            u_c = self.useable

            if u_c.on_use_effect.get('effect_name') is not None:
                 listing += f"\n\n Effect: %{col}%{u_c.on_use_effect.get('effect_name').title()}%%"

            if u_c.on_use_params.get('pwr') is not None:
                pwr = u_c.on_use_params.get('pwr')
                if isinstance(pwr, int):
                    listing += f"\n\n Power: %{col}%{pwr}%%"
                else:
                    listing += f"\n\n Power: %{col}%{pwr[0]}-{pwr[1]}%%"

            if u_c.on_use_params.get('radius') is not None:
                listing += f"\n\n Range: %{col}%{u_c.on_use_params.get('radius')}%%"

            if u_c.on_use_params.get('range') is not None:
                u_range = u_c.on_use_params.get('range')
                listing += f"\n\n Range: %{col}%{u_range[0]}-{u_range[1]}%%"
        
        return listing

    # Convenience #
    @property
    def name(self):
        return self.owner.name