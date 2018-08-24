from gui.messages import Message


class Item:
    def __init__(self, useable=None, equipment=None):
        self.useable = useable
        self.equipment = equipment

        if self.useable:
            useable.owner = self

        if self.equipment:
            equipment.owner = self

    @property
    def attr_list(self):
        """
        :return:
        :rtype: list
        """
        list = ['']

        if self.equipment.e_type:
            list.append(f' Type: {self.equipment.e_type.capitalize()}')

        if self.equipment.e_to:
            list.append(f' Equips To: {self.equipment.e_to.capitalize()}')

        if self.equipment.av:
            list.append(f' Armor: {self.equipment.av}')

        if self.equipment.dmg_range:
            list.append(f' Damage Potential: {self.equipment.dmg_range[0]}-{self.equipment.dmg_range[1]}')

        if self.equipment.l_radius:
            list.append(f' Light Radius: {self.equipment.l_radius}')

        return list