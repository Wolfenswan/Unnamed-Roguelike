from random import randint, choice

import logging

from config_files import colors
from gameobjects.entity import Entity
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_order import RenderOrder


class Fighter:
    def __init__(self, hp, stamina, defense, power, vision):
        """

        :param hp:
        :type hp: int
        :param stamina:
        :type stamina: int
        :param defense:
        :type defense: int
        :param power:
        :type power: int
        :param vision:
        :type vision: int

        """
        self.max_hp = hp
        self.hp = hp
        self.max_stamina = stamina
        self.stamina = stamina
        self.base_defense = defense
        self.base_power = power
        self.base_vision = vision

        self.is_blocking = False

    @property
    def power(self): # TODO placeholder - later weapon damage should be separated from fighter power
        power = self.base_power
        for e in self.owner.paperdoll.equipped_items:
            dmg_range = vars(e.item.equipment).get('dmg_range')
            # This extra step is required as av value is set as None for all Equipments during data processing
            if dmg_range:
                power += randint(*dmg_range)
        return power

    @property
    def defense(self):
        defense = self.base_defense
        for e in self.owner.paperdoll.equipped_items:
            av = vars(e.item.equipment).get('av')
            # This extra step is required as av value is set as None for all Equipments during data processing
            if av:
                defense += av
        return defense

    @property
    def vision(self):
        vision = self.base_vision
        for e in self.owner.paperdoll.equipped_items:
            l_radius = vars(e.item.equipment).get('l_radius')
            # This extra step is required as l_radius value is set as None for all Equipments during data processing
            if l_radius:
                vision += l_radius
        return vision

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

        logging.debug(f'{self.owner.name.capitalize()} attacks {target.name.capitalize()} with {self.power} power against {target.fighter.defense} defense for {damage} damage.')

        # TODO if blocked, reduce stamina
        if damage > 0:
            if target.fighter.is_blocking and target.fighter.stamina > 0:
                results.extend(target.fighter.block(damage))
            else:
                msg_type = MessageType.ALERT if target.is_player else MessageType.COMBAT
                results.append({'message': Message(
                    f'{self.owner.name.capitalize()} attacks {target.name.capitalize()} for {str(damage)} hit points.', type=msg_type)})
                results.extend(target.fighter.take_damage(damage))
        else:
            results.append(
                {'message': Message(f'{self.owner.name.capitalize()} attacks {target.name} but does no damage.', type=MessageType.COMBAT)})

        return results

    def block(self, damage):
        results = []
        self.stamina -= damage
        if self.owner.is_player:
            message = Message(f'You were able to block the attack!', type=MessageType.GOOD)
        else:
            message = Message(f'{self.owner.name.capitalize()} was able to block the attack!', type=MessageType.COMBAT)
        results.append({'message': message})
        return results

    def toggle_blocking(self):
        self.is_blocking = not self.is_blocking

    def death(self, game):
        ent = self.owner
        x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = colors.corpse
        ent.color_bg = colors.black
        game.map.tiles[x][y].gibbed = True

        if ent.is_player:
            message = Message('You died!', type=MessageType.BAD)
        else:
            message = Message(f'The {ent.name.capitalize()} is dead!', type=MessageType.GOOD, category=MessageCategory.OBSERVATION)

            ent.blocks = False
            ent.render_order = RenderOrder.CORPSE
            ent.fighter = None
            ent.ai = None
            ent.name = f'Remains of a {ent.name}'

        # Create gibs
        # TODO Consider force of impact (amount of damage done beyond 0 hp?) to vary spread
        for i in range(1, randint(2, 4)):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            game.map.tiles[c_x][c_y].gibbed = True
            if not game.map.tiles[c_x][c_y].blocked and randint(0, 100) > 85:
                c = Entity(c_x, c_y, '~', colors.corpse, f'Bits of a {ent.name}')
                c.render_order = RenderOrder.CORPSE
                game.entities.append(c)

        return message
