class Equipment():

    def __init__(self, e_to, dmg_range = None, av = None, qu_slots = None, l_radius = None, moveset = None):
        self.e_to = e_to
        self.dmg_range = dmg_range
        self.av = av
        self.qu_slots = qu_slots
        self.l_radius = l_radius
        self.moveset = moveset
        if self.moveset:
            self.moveset = self.moveset()