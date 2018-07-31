class Equipment():

    def __init__(self, e_to, e_type, dmg_range = None, av = None, qu_slots = None, l_radius = None):
        self.e_to = e_to
        self.e_type = e_type
        self.dmg_range = dmg_range
        self.av = av
        self.qu_slots = qu_slots
        self.l_radius = l_radius
        self.on_equip = None
        self.on_dequip = None