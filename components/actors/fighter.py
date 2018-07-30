from random import randint

import tcod
import logging

from config_files import colors
from gameobjects.entity import Entity
from gui.messages import Message, MessageType
from rendering.render_order import RenderOrder


class Fighter:
    def __init__(self, hp, defense, power, vision):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power
        self.vision = vision

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

        logging.debug(f'({self} was healed for {amount}.')

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message(f'{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.')})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message(f'{self.owner.name.capitalize()} attacks {target.name} but does no damage.')})

        return results

    def death(self,map):
        ent = self.owner
        x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = colors.corpse
        map.tiles[x][y].gibbed = True
        
        if ent.is_player:
            message = Message('You died!', msg_type=MessageType.INFO_BAD)
        else:
            message = Message(f'The {ent.name.capitalize()} is dead!', MessageType.INFO_GOOD)

            ent.blocks = False
            ent.render_order = RenderOrder.CORPSE
            ent.fighter = None
            ent.ai = None
            ent.name = f'Remains of a {ent.name}'

        # Create gibs
        # TODO Consider force of impact (amount of damage done beyond 0 hp?) to vary spread
        for i in range(1, randint(2, 4)):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            map.tiles[c_x][c_y].gibbed = True
            if randint(0, 100) > 10:
                c = Entity('~', c_x, c_y, colors.corpse, f'Bits of a {ent.name}', 'Assorted offal.')
                c.render_order = RenderOrder.CORPSE

        return message