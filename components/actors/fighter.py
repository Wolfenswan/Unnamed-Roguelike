from random import randint, choice

import logging

from components.actors.status_modifiers import Presence, Surrounded
from config_files import colors
from data.actor_data.act_status_mod import status_modifiers_data
from data.data_types import AttackType
from data.item_data.wp_attacktypes import wp_attacktypes_data
from data.gui_data.gui_fighter import atkdmg_string_data, stadmg_string_data, sta_color_data, stadmg_color_data
from gameobjects.block_level import BlockLevel
from gameobjects.entity import Entity
from gameobjects.util_functions import entity_at_pos
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_line
from rendering.render_order import RenderOrder


class Fighter:
    def __init__(self, hp, stamina, base_av, base_strength, base_vision):
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
        self.__hp = hp
        self.max_hp = hp
        self.__stamina = stamina
        self.max_stamina = stamina
        self.__base_av = base_av
        self.__base_strength = base_strength
        self.__base_vision = base_vision

        self.surrounded = Surrounded.FREE
        self.is_blocking = False
        self.presence = {
            Presence.DAZED: False,
            Presence.STUNNED: False
        }

    @property
    def hp(self):
        return self.__hp

    @property
    def hp_string(self):
        percentage = (self.__hp / self.max_hp * 100)
        if 86.0 <= percentage:
            return 'healthy'
        elif 71.0 <= percentage:
            return 'scratched'
        elif 15.0 <= percentage:
            return 'wounded'
        elif 1.0 <= percentage:
            return 'near death'
        else:
            return 'dead'

    @property
    def hp_color(self):
        percentage = (self.__hp / self.max_hp * 100)
        if 86.0 <= percentage:
            return colors.dark_green
        elif 71.0 <= percentage:
            return colors.darkest_green
        elif 15.0 <= percentage:
            return colors.dark_red
        elif 1.0 <= percentage:
            return colors.darker_red
        else:
            return colors.darkest_red

    @hp.setter
    def hp(self, value):
        value = round(value)
        if value < 0:
            self.__hp = 0
        elif value > self.max_hp:
            self.__hp = self.max_hp
        else:
            self.__hp = value

    @property
    def stamina(self):
        return self.__stamina

    @property
    def stamina_string(self):
        percentage = (self.__stamina / self.max_stamina * 100)
        if 90.0 <= percentage:
            return 'fit'
        elif 60.0 <= percentage:
            return 'active'
        elif 30.0 <= percentage:
            return 'strained'
        elif 15.0 <= percentage:
            return 'spent'
        else:
            return 'exhausted'

    @property
    def stamina_color(self):
        percentage = (self.__stamina / self.max_stamina * 100)
        if 90.0 <= percentage:
            return sta_color_data[90]
        elif 60.0 <= percentage:
            return sta_color_data[60]
        elif 30.0 <= percentage:
            return sta_color_data[30]
        elif 15.0 <= percentage:
            return sta_color_data[15]
        else:
            return sta_color_data[1]

    @stamina.setter
    def stamina(self, value):
        value = round(value)
        if value < 0:
            self.__stamina = 0
        elif value > self.max_stamina:
            self.__stamina = self.max_stamina
        else:
            self.__stamina = value

    @property
    def strength(self):
        return self.__base_strength

    @property
    def base_dmg_potential(self):
        """
        Attribute returns the entity's current damage potential (base + weapon)
        as tuple with the fighter's base str added.
        :return: tuple of min/max damage
        :rtype: tuple
        """
        if self.weapon:
            return (self.strength+self.weapon.dmg_potential[0], self.strength + (self.weapon.dmg_potential[1]))
        return (self.strength, self.strength)

    @property
    def modded_dmg_potential(self):
        w_mod = 1
        p_mod = 1

        if self.weapon:
            w_mod = self.weapon.moveset.dmg_multipl

        if self.presence[Presence.DAZED]:
            p_mod = status_modifiers_data[Presence.DAZED]['dmg_multipl']

        if self.presence[Presence.STUNNED]:
            p_mod = status_modifiers_data[Presence.STUNNED]['dmg_multipl']

        return (round(self.base_dmg_potential[0] * w_mod * p_mod), round(self.base_dmg_potential[-1] * w_mod * p_mod))

    @property
    def dmg_roll(self):
        return randint(*self.modded_dmg_potential)

    @property
    def defense(self):
        total_defense = self.__base_av
        for e in self.owner.paperdoll.equipped_items:
            av = vars(e.item.equipment).get('av')
            # This extra step is required as av value is set to None for all Equipments during data processing
            if av:
                total_defense += av

        return total_defense
    
    @property
    def modded_defense(self):
        modded_def = self.defense
        if self.presence[Presence.DAZED]:
            modded_def *= status_modifiers_data[Presence.DAZED]['av_multipl']

        if self.presence[Presence.STUNNED]:
            modded_def *= status_modifiers_data[Presence.STUNNED]['av_multipl']

        if self.surrounded != Surrounded.FREE:
            modded_def *= status_modifiers_data[self.surrounded]['av_multipl']

        return round(modded_def)

    @property
    def modded_block_def(self):
        block_def = self.shield.block_def
        if self.surrounded == Surrounded.THREATENED:
            block_def = round(block_def * 0.75)
        if self.surrounded == Surrounded.OVERWHELMED:
            block_def = 0
        return block_def
    
    @property
    def vision(self):
        vision = self.__base_vision
        for e in self.owner.paperdoll.equipped_items:
            l_radius = vars(e.item.equipment).get('l_radius')
            # This extra step is required as l_radius value is set to None for all Equipments during data processing
            if l_radius:
                vision += l_radius
        return vision

    @property
    def weapon(self):
        """
        :return: Equipment component of currently equipped weapon.
        """
        weapon_ent = self.owner.paperdoll.weapon_arm.weapon # TODO add check for 2nd hand after implementing dual wielding
        if weapon_ent:
            return weapon_ent.item.equipment
        else:
            return None

    @property
    def shield(self):
        """
        :return: Equipment component of currently equipped shield (or parrying weapon).
        """
        shield_ent = self.owner.paperdoll.shield_arm.shield  # TODO add check for 2nd hand after implementing dual wielding
        if shield_ent:
            return shield_ent.item.equipment
        else:
            return None
        
    @staticmethod
    def atk_dmg_string(damage, target_max_hp):
        percentage = (damage / target_max_hp * 100)
        if 90 <= percentage:
            return choice(atkdmg_string_data[90])
        elif 65.0 <= percentage:
            return choice(atkdmg_string_data[65])
        elif 45.0 <= percentage:
            return choice(atkdmg_string_data[45])
        elif 25.0 <= percentage:
            return choice(atkdmg_string_data[25])
        elif 5.0 <= percentage:
            return choice(atkdmg_string_data[5])
        elif 1.0 <= percentage:
            return choice(atkdmg_string_data[1])
        else:
            return 'no'
        
    @staticmethod
    def sta_dmg_string(damage, target_max_stamina):
        percentage = (damage / target_max_stamina * 100)
        if 90 <= percentage:
            return choice(stadmg_string_data[90])
        elif 65.0 <= percentage:
            return choice(stadmg_string_data[65])
        elif 45.0 <= percentage:
            return choice(stadmg_string_data[45])
        elif 25.0 <= percentage:
            return choice(stadmg_string_data[25])
        elif 5.0 <= percentage:
            return choice(stadmg_string_data[5])
        elif 1.0 <= percentage:
            return choice(stadmg_string_data[1])
        else:
            return 'no'
        
    @staticmethod
    def stadmg_color(damage, target_max_stamina):
        percentage = (damage / target_max_stamina * 100)
        if 90 <= percentage:
            return stadmg_color_data[90]
        elif 65.0 <= percentage:
            return stadmg_color_data[65]
        elif 45.0 <= percentage:
            return stadmg_color_data[45]
        elif 25.0 <= percentage:
            return stadmg_color_data[25]
        elif 5.0 <= percentage:
            return stadmg_color_data[5]
        elif 1.0 <= percentage:
            return stadmg_color_data[1]

    def check_surrounded(self, game):
        nearby_enemies = len(self.owner.enemies_in_distance(game.npc_ents, dist=1.5))
        if nearby_enemies < 3:
            return Surrounded.FREE
        elif nearby_enemies < 5:
            return Surrounded.THREATENED
        else:
            return Surrounded.OVERWHELMED

    #################################
    # ATTRIBUTE MODIFYING FUNCTIONS #
    #################################

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

    def recover(self, amount):
        self.stamina += amount
        if self.stamina > self.max_stamina:
            self.stamina = self.max_stamina
        logging.debug(f'({self} recovered stamina for {amount}.')

    def exert(self, string, amount):
        self.stamina -= amount
        logging.debug(f'{self.owner.name} exerted by {string} for {amount}')
        #pronoun = 'Your' if self.owner.isplayer else 'The'
        if self.owner.is_player:
            sta_dmg_string = self.sta_dmg_string(amount, self.max_stamina)
            col = self.stadmg_color(amount, self.max_stamina)
            message = Message(f'You {string} for %{col}%{sta_dmg_string}%c exertion.', category=MessageCategory.OBSERVATION,
                              type=MessageType.COMBAT_INFO)
            return {'message': message}
        return {}

    def set_presence(self, presence, value, duration=0):
        self.presence[presence] = value
        if duration > 0:
            self.owner.actionplan.add_to_queue(execute_in=duration,
                                               planned_function=self.set_presence,
                                               planned_function_args=(presence, False))


    ############################
    # ATTACK RELATED FUNCTIONS #
    ############################

    def attack_setup(self, target, game, mod=1):
        results = []
        blocked = False
        attack_string = 'hits'
        extra_targets = []

        if self.weapon:
            move_results = self.weapon.moveset.execute(self.owner, target)
            attack_string = move_results.get('string', 'hits')
            extra_targets = move_results.get('extra_targets', [])

        attack_power = self.dmg_roll * mod

        logging.debug(f'{self.owner.name} prepares to attack {target.name} with base damage {self.base_dmg_potential},'
                      f' (modded {self.modded_dmg_potential}) for a power of {attack_power}')

        if self.stamina < attack_power/3:
            message = Message(f'PLACEHOLDER: Attacking without enough Stamina!', category=MessageCategory.COMBAT,
                              type=MessageType.SYSTEM)
            results.append({'message': message})
            return results

        if target.fighter.stamina <= 0: # If the target is out of stamina, attack power is doubled
            attack_power *= 2

        if target.fighter.is_blocking:
            blocked = target.fighter.attempt_block(self, attack_power)

        if blocked: # Block exertion
            sta_dmg = round(attack_power / 2)
            mod = wp_attacktypes_data[self.weapon.attack_type].get('block_sta_dmg_multipl', 1)
            sta_dmg = round(sta_dmg * mod)
            logging.debug(f'{target.name} block exert multiplied by {mod} due to {self.owner.name} attack type {self.weapon.attack_type}')
            results.append(target.fighter.exert('block', sta_dmg))

            if target.is_player:
                message = Message(f'You block the attack, dazing the {self.owner.name.title()}!',
                                  category=MessageCategory.COMBAT, type=MessageType.COMBAT_GOOD)
            else:
                message = Message(f'The {self.owner.name.title()} blocks your attack, dazing you!',
                                  category=MessageCategory.COMBAT, type=MessageType.COMBAT_BAD)

            self.set_presence(Presence.DAZED, True, 1)
            results.append({'message': message})
        else:
            results.extend(self.attack_execute(target, attack_power, attack_string))

        for target_pos in extra_targets:
            if entity_at_pos(game.npc_ents, *target_pos):
                extra_target = entity_at_pos(game.npc_ents, *target_pos) # TODO Currently ignores blocking
                results.extend(self.attack_execute(extra_target, attack_power//2, 'further hits'))

        self.exert('attack',attack_power/3)
        return results

    def attack_execute(self, target, power, attack_string):
        results = []

        damage = round(power - (target.fighter.modded_defense))

        if target == self.owner:
            target_string = 'itself'
        elif target.is_player:
            target_string = 'you'
        else:
            target_string = f'the {target.name.title()}'

        if damage > 0:
            msg_type = MessageType.COMBAT_BAD if target.is_player else MessageType.COMBAT_INFO

            atk_dmg_string = self.atk_dmg_string(damage, target.fighter.max_hp)
            results.append({'message': Message(
                f'{self.owner.name} {attack_string} {target_string}, {choice(atkdmg_string_data["verbs"])} {atk_dmg_string} damage.', category=MessageCategory.COMBAT, type=msg_type)})
            results.extend(target.fighter.take_damage(damage))
        else:
            msg_type = MessageType.COMBAT_BAD if not target.is_player else MessageType.COMBAT_GOOD
            results.append(
                {'message': Message(f'{self.owner.name.title()} {attack_string} {target_string} but can not pierce armor.', category=MessageCategory.COMBAT, type=msg_type)})
            results.append(target.fighter.exert('armor deflection', power))

        logging.debug(
            f'{self.owner.name.title()} attacks {target.name.title()} with {power} power against {target.fighter.defense} defense for {damage} damage. Target has {target.fighter.stamina} stamina left.)')
        return results

    #############################
    # DEFENSE RELATED FUNCTIONS #
    #############################

    def toggle_blocking(self):
        self.is_blocking = not self.is_blocking

    def attempt_block(self, attacker, damage):
        block_def = self.modded_block_def

        if damage <= block_def:
            return True
        elif damage <= block_def * 2:
            chance = self.block_chance(attacker.weapon.attack_type, damage)
            print(chance)
            if chance > 0 and chance >= randint(0,100):
                return True
        return False

    def block_chance(self, attack_type, damage):
        """
        Returns the chance to block a strike that surpasses an entitiess's block defense.
        It is possible to block up to the double of maximum block defense.
        """
        block_def = self.shield.block_def
        mod = wp_attacktypes_data[attack_type].get('block_def_multipl',1)
        block_def = round(block_def * mod)
        logging.debug(f'{self.owner.name} block def. multiplied by {mod} due to attack type {attack_type}')

        if block_def > 0:
            return 101 - ((damage - block_def) / block_def * 100)
        else:
            return 0

    def average_chance_to_block(self, attacker, debug=False):
        """
        Utility function for debug information and an entities description window.
        """
        average = 0
        dmg_range = attacker.fighter.base_dmg_potential
        for dmg in dmg_range:
            average += self.block_chance(attacker.fighter.weapon.attack_type, dmg)
        average /= len(dmg_range)

        if debug:
            return average
        else:
            if average >= 100:
                return 'guaranteed'
            elif average >= 75:
                return 'very easy'
            elif average >= 50:
                return 'doable'
            elif average >= 25:
                return 'hard'
            elif average >= 5:
                return 'very hard'
            else:
                return 'impossible'

    def dodge(self, dx, dy, game):
        results = []
        exertion = self.defense * 2
        if self.stamina >= exertion:
            animate_move_line(self.owner, dx, dy, 2, game, anim_delay=0.05)
            results.append(self.exert('dodge', exertion))
        else:

            results.append({'message':Message('PLACEHOLDER: Stamina too low to dodge!')})
        return results

    def death(self, game):

        if game.debug['invin'] and self.owner.is_player:
            self.owner.fighter.hp = self.owner.fighter.max_hp

        ent = self.owner
        ent.ai = None
        x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = colors.corpse
        ent.color_bg = colors.black
        game.map.tiles[(x,y)].gibbed = True

        # Create gibs
        # TODO Consider force of impact (amount of damage done beyond 0 hp?) to vary spread
        for i in range(1, randint(2, 4)):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            game.map.tiles[(c_x,c_y)].gibbed = True
            if not game.map.tiles[(c_x,c_y)].blocked and randint(0, 100) > 85:
                c = Entity(c_x, c_y, '~', colors.corpse, f'{ent.name.title()} bits', is_corpse=True)
                c.render_order = RenderOrder.CORPSE
                game.entities.append(c)

        if ent.is_player:
            message = Message('You died!', type=MessageType.BAD)
        else:
            message = Message(f'The {ent.name.title()} is dead!', type=MessageType.GOOD, category=MessageCategory.OBSERVATION)

            ent.render_order = RenderOrder.CORPSE
            ent.blocks[BlockLevel.WALK] = False
            ent.ai = None
            ent.is_corpse = True
            #ent.name = f'{ent.name.title()} remains'

        return message
