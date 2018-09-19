from components.items.moveset import Moveset


class Equipment():

    def __init__(self, e_to, dmg_range = None, av = None, qu_slots = None, l_radius = None, two_handed = False, moveset = None):
        self.e_to = e_to
        self.dmg_range = dmg_range
        self.av = av
        self.qu_slots = qu_slots
        self.l_radius = l_radius
        self.two_handed = two_handed
        self.moveset = moveset
        if self.moveset:
            self.moveset = Moveset(self.moveset)

    @property
    def name(self):
        return self.owner.owner.name

    @property
    def full_name(self):
        return self.owner.owner.full_name

    @property
    def color(self):
        return self.owner.owner.color