import tcod

from gui.messages import Message, MessageType
from rendering.render_order import RenderOrder


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message(f'{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.')})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message(f'{self.owner.name.capitalize()} attacks {target.name} but does no damage.')})

        return results

    def death(self):
        # TODO gibbing
        ent = self.owner
        
        if ent.is_player:
            ent.char = '%'
            ent.color = tcod.dark_red

            message = Message('You died!', msg_type=MessageType.INFO_BAD)
        else:
            
            ent.char = '%'
            ent.color = tcod.dark_red
            ent.blocks = False
            ent.render_order = RenderOrder.CORPSE
            ent.fighter = None
            ent.ai = None
            ent.name = 'remains of ' + ent.name

            message = Message(f'The {ent.name.capitalize()} is dead!', MessageType.INFO_GOOD)

        return message