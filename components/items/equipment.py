from dataclasses import dataclass

from components.items.moveset import Moveset


@dataclass
class Equipment():
    e_to: str
    dmg_potential: tuple = None
    av: int = None
    block_def: int = None
    qu_slots: int = None
    l_radius: int = None
    two_handed: bool = None
    attack_type: str = None
    moveset: Moveset = None

    @property
    def name(self):
        return self.owner.owner.name

    @property
    def full_name(self):
        return self.owner.owner.full_name

    @property
    def color(self):
        return self.owner.owner.color