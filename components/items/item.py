from gui.messages import Message


class Item:
    def __init__(self, useable=None, equipment=None):
        self.useable = useable
        self.equipment = equipment

        if self.useable:
            useable.owner = self

        if self.equipment:
            equipment.owner = self