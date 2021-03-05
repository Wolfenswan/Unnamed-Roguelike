from typing import Optional, Tuple

from dataclasses import dataclass

from components.items.moveset import Moveset
from data.data_enums import ItemType


@dataclass
class Equipment():
    e_to: str
    dmg_potential: Optional[Tuple]
    av: Optional[int]
    block_def: Optional[int]
    qu_slots: Optional[int]
    attack_range: Optional[Tuple]
    l_radius: Optional[int]
    two_handed: Optional[bool]
    one_handed_penalty_mod: Optional[int]  # if a two-handed weapon can be wielded in one hand with penalties
    moveset: Optional[Moveset]
    owner:Optional = None

    def __repr__(self):
        return f'Equipment:{id(self)} ({self.owner.name})'

    def __post_init__(self):
        if self.moveset:
            self.moveset.owner = self

    @property
    def name(self):
        return self.owner.owner.name

    @property
    def full_name(self):
        return self.owner.owner.full_name

    @property
    def color(self):
        return self.owner.owner.color

    @property
    def two_handed_only(self):
        return self.two_handed and self.one_handed_penalty_mod is None