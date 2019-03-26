from random import randint, choice

import logging

from dataclasses import dataclass

from components.actors.fighter_util import DamagePercentage, AttributePercentage, get_gui_data
from components.actors.status_modifiers import Presence, Surrounded
from components.statistics import statistics_updater
from config_files import colors
from data.actor_data.act_status_mod import status_modifiers_data
from data.data_types import ItemType
from data.item_data.wp_attacktypes import wp_attacktypes_data
from data.gui_data.gui_fighter import hpdmg_string_data, stadmg_string_data, sta_color_data, stadmg_color_data, \
    sta_string_data, hpdmg_color_data, hp_string_data, hp_color_data
from gameobjects.block_level import BlockLevel
from gameobjects.util_functions import entity_at_pos, line_between_pos
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_projectile
from rendering.render_order import RenderOrder

@dataclass
class Fighter:
    __hp:int
    __stamina:int
    __base_av:int
    __base_strength:int
    __base_vision:int

    def __post_init__(self):
        self.active_weapon = None
        self.max_hp = self.__hp
        self.max_stamina = self.__stamina
        self.surrounded = Surrounded.FREE
        self.is_blocking = False
        self.is_dodging = False
        self.presence = {
            Presence.DAZED: False,
            Presence.STUNNED: False
        }

    ##############
    # ATTRIBUTES #
    ##############

    @property
    def hp(self):
        return self.__hp

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
    def hp_full(self):
        return self.hp == self.max_hp

    @property
    def hp_string(self):
        percentage = (self.__hp / self.max_hp * 100)
        return get_gui_data(percentage, hp_string_data, AttributePercentage)

    @property
    def hp_color(self):
        percentage = (self.__hp / self.max_hp * 100)
        return get_gui_data(percentage, hp_color_data, AttributePercentage)

    @property
    def stamina(self):
        return self.__stamina

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
    def sta_full(self):
        return self.stamina == self.max_stamina

    @property
    def stamina_string(self):
        percentage = (self.__stamina / self.max_stamina * 100)
        return get_gui_data(percentage, sta_string_data, AttributePercentage)

    @property
    def stamina_color(self):
        percentage = (self.__stamina / self.max_stamina * 100)
        return get_gui_data(percentage, sta_color_data, AttributePercentage)

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
        if self.active_weapon is not None:
            return (self.strength + self.active_weapon.dmg_potential[0], self.strength + (self.active_weapon.dmg_potential[1]))
        return (self.strength, self.strength)

    @property
    def modded_dmg_potential(self):
        w_mod = 1
        p_mod = 1

        if self.active_weapon is not None:
            w_mod = self.active_weapon.moveset.dmg_multipl

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
    def can_dodge(self):
        exertion = self.defense * 2
        return self.stamina >= exertion
    
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
    def weapon_melee(self):
        """
        :return: Currently equipped melee weapon entity
        """
        weapon_ent = self.owner.paperdoll.weapon_arm.melee_weapon # TODO add check for 2nd hand after implementing dual wielding
        if weapon_ent:
            return weapon_ent
        else:
            return None

    @property
    def weapon_ranged(self):
        """
        :return: Currently equipped ranged weapon entity
        """
        weapon_ent = self.owner.paperdoll.weapon_arm.ranged_weapon
        if weapon_ent:
            return weapon_ent
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

    def hpdmg_string(self, damage):
        percentage = (damage / self.max_hp * 100)
        return choice(get_gui_data(percentage, hpdmg_string_data, DamagePercentage))

    def hpdmg_color(self, damage):
        percentage = (damage / self.max_hp * 100)
        return get_gui_data(percentage, hpdmg_color_data, DamagePercentage)

    def stadmg_string(self, damage):
        percentage = (damage / self.max_stamina * 100)
        return choice(get_gui_data(percentage, stadmg_string_data, DamagePercentage))

    def stadmg_color(self, damage):
        percentage = (damage / self.max_stamina * 100)
        return get_gui_data(percentage, stadmg_color_data, DamagePercentage)

    def check_surrounded(self, game):
        nearby_enemies = len(self.owner.surrounding_enemies(game.npc_ents))
        if nearby_enemies < 3:
            return Surrounded.FREE
        elif nearby_enemies < 5:
            return Surrounded.THREATENED
        else:
            return Surrounded.OVERWHELMED

    #################################
    # ATTRIBUTE MODIFYING FUNCTIONS #
    #################################

    @statistics_updater('hp_change', substract=True)
    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner})
        return results

    @statistics_updater('hp_change')
    def heal(self, amount):
        self.hp += amount
        logging.debug(f'({self} was healed for {amount}.')

    @statistics_updater('sta_change')
    def recover(self, amount):
        self.stamina += amount
        logging.debug(f'({self} recovered stamina for {amount}.')

    @statistics_updater('sta_change', substract=True)
    def exert(self, amount, string='action'):
        self.stamina -= round(amount)
        logging.debug(f'{self.owner.name} exerted by {string} for {amount}')
        #pronoun = 'Your' if self.owner.isplayer else 'The'
        if self.owner.is_player:
            sta_dmg_string = self.stadmg_string(amount)
            col = self.stadmg_color(amount)
            message = Message(f'%white%You%% {string} for %{col}%{sta_dmg_string}%% exertion.',
                              category=MessageCategory.OBSERVATION, type=MessageType.COMBAT_INFO)
            return {'message': message}
        return {}

    def set_presence(self, presence:Presence, value:int, duration:int=0):
        self.presence[presence] = value
        if duration > 0: # If duration > 0, set a plan to disable the current presence in n turns
            self.owner.actionplan.add_to_queue(execute_in=duration,
                                               planned_function=self.set_presence,
                                               planned_function_args=(presence, False))

    def toggle_weapon(self):
        if (self.weapon_melee is not None and self.weapon_ranged is not None):
            if self.active_weapon == self.weapon_melee:
                self.active_weapon = self.weapon_ranged
            else:
                self.active_weapon = self.weapon_melee
        else:
            if self.weapon_melee is not None:
                self.active_weapon = self.weapon_melee
            elif self.weapon_ranged is not None:
                self.active_weapon = self.weapon_ranged
            else:
                self.active_weapon = None
        return self.active_weapon

    ############################
    # ATTACK RELATED FUNCTIONS #
    ############################

    def attack_setup(self, target, game, dmg_mod_multipl=1, verb:str='hits', ignore_moveset:bool=False, ranged_projectile:bool=True):
        results = []
        blocked = False
        extra_attacks = []

        melee = True if self.active_weapon.type == ItemType.MELEE_WEAPON else False

        if ignore_moveset:
            attack_power = choice(self.base_dmg_potential) * dmg_mod_multipl
            attack_exertion = attack_power / 3
        else:
            if self.active_weapon is not None:
                move_results = self.active_weapon.moveset.execute(self.owner, target)
                verb = move_results.get('attack_verb', 'hits')
                extra_attacks = move_results.get('extra_attacks', [])
            else:
                verb = 'pummels'

            attack_power = self.dmg_roll * dmg_mod_multipl
            attack_exertion = attack_power / 3 * self.active_weapon.moveset.exert_multipl
            self.active_weapon.moveset.cycle_moves()

        if not melee:
            logging.debug(f'{self.owner} is attempting ranged attack at {target}')
            if not self.owner.free_line_to_ent(target, game):
                pos_list = line_between_pos(*self.owner.pos, *target.pos)
                try:
                    obstacle = next(entity_at_pos(game.blocking_ents, *pos) for pos in pos_list if entity_at_pos(game.blocking_ents, *pos) is not None)
                    logging.debug(f'{obstacle} is blocking direct los')
                    if randint(0,1): # TODO can later be modified by skill level, attributes etc.
                        message = Message(f'PLACEHOLDER: {self.owner.name} hits {obstacle.name} instead of {target.name}!',
                                          category=MessageCategory.COMBAT,
                                          type=MessageType.SYSTEM)
                        results.append({'message': message})
                        target = obstacle
                except:
                    return results

            if ranged_projectile:
                animate_projectile(*self.owner.pos,*target.pos,game, color=colors.beige) # TODO color can later be modified by weapon/ammo

        logging.debug(f'{self.owner.name} prepares to attack {target.name} with base damage {self.base_dmg_potential},'
                      f' (modded {self.modded_dmg_potential}) for a power of {attack_power}')

        if self.stamina < attack_power / 3:
            message = Message(f'PLACEHOLDER: Attacking without enough Stamina!', category=MessageCategory.COMBAT,
                              type=MessageType.SYSTEM)
            results.append({'message': message})
            return results

        if target.fighter.stamina <= 0:  # If the target is out of stamina, attack power is doubled
            attack_power *= 2

        if target.fighter.is_blocking:
            blocked = target.fighter.attempt_block(self, attack_power)

        if blocked:  # TODO move to own function
            sta_dmg = round(attack_power / 2) # TODO should attacker also take sta damage?
            dmg_mod_multipl = wp_attacktypes_data[self.active_weapon.attack_type].get('block_sta_dmg_multipl', 1)
            sta_dmg = round(sta_dmg * dmg_mod_multipl)
            logging.debug(
                f'{target.name} block exert multiplied by {dmg_mod_multipl} due to {self.owner.name} attack type {self.active_weapon.attack_type}')
            results.append(target.fighter.exert(sta_dmg, 'block'))

            if melee:
                if target.is_player:
                    message = Message(f'You block the attack, dazing the {self.owner.name_with_color}!',
                                      category=MessageCategory.COMBAT, type=MessageType.COMBAT_GOOD)
                else:
                    message = Message(f'The {self.owner.name_with_color} blocks your attack, dazing you!',
                                      category=MessageCategory.COMBAT, type=MessageType.COMBAT_BAD)

                self.set_presence(Presence.DAZED, True, 1)
                results.append({'message': message})
        else:
            results.extend(self.attack_execute(target, attack_power, verb))

        for attack_pos in extra_attacks:
            extra_target = entity_at_pos(game.npc_ents, *attack_pos)
            if extra_target:
                results.extend(self.attack_execute(extra_target, attack_power // 2, 'further hits'))

        self.exert(attack_exertion, 'attack')

        return results

    def attack_execute(self, target, power, attack_string):
        results = []

        damage = round(power - (target.fighter.modded_defense))

        if target == self.owner:
            target_string = 'itself'
        else:
            target_string = target.address_with_color

        if damage > 0:
            msg_type = MessageType.COMBAT_BAD if target.is_player else MessageType.COMBAT_INFO
            atk_dmg_string = target.fighter.hpdmg_string(damage)
            col = target.fighter.hpdmg_color(damage)
            results.append({'message': Message(
                f'{self.owner.name_with_color} {attack_string} {target_string}, {choice(hpdmg_string_data["verbs"])} %{col}%{atk_dmg_string}%% damage.', category=MessageCategory.COMBAT, type=msg_type)})
            results.extend(target.fighter.take_damage(damage))

            # STATISTICS
            self.owner.statistics.dmg_done += damage
            if target.fighter.hp <= 0:
                self.owner.statistics.killed += [target.name]

        else:
            msg_type = MessageType.COMBAT_BAD if not target.is_player else MessageType.COMBAT_GOOD
            results.append(
                {'message': Message(f'{self.owner.name_with_color} {attack_string} {target_string} but can not pierce armor.', category=MessageCategory.COMBAT, type=msg_type)})
            results.append(target.fighter.exert(power, 'armor deflection'))

        logging.debug(
            f'{self.owner.name.title()} attacks {target.name.title()} with {power} power against {target.fighter.defense} defense for {damage} damage. Target has {target.fighter.stamina} stamina left.)')
        return results

    #############################
    # DEFENSE RELATED FUNCTIONS #
    #############################

    def toggle_blocking(self):
        results = []

        if self.is_blocking:
            results.append({'message': Message('You stop blocking.', type=MessageType.COMBAT_INFO)})
            self.is_blocking = False
        elif self.shield:
            results.append({'message': Message(f'You ready your {self.shield.name}.', type=MessageType.COMBAT_INFO)})
            self.is_blocking = True
        else:
            results.append({'message': Message('You need a shield to block.', type=MessageType.COMBAT_INFO)})

        return results


    def toggle_dodging(self):
        results = []

        if self.is_dodging:
            results.append({'message': Message('You stop dodging.', type=MessageType.COMBAT_INFO)})
            self.is_dodging = False
        else:
            results.append({'message': Message('You start dodging.', type=MessageType.COMBAT_INFO)})
            self.is_dodging = True

        return results


    def attempt_block(self, attacker, damage):
        """
        If an actor's blocking defense is greater than the inflicted damage, all damage is nullified. Otherwise there
        is a diminishing chance to block up to double of the block defense.
        """
        block_def = self.modded_block_def

        if damage <= block_def:
            return True
        elif damage <= block_def * 2:
            chance = self.block_chance(attacker.active_weapon.attack_type, damage)
            if chance > 0 and chance >= randint(0,100):
                return True
        return False

    def block_chance(self, attack_type, damage):
        """
        Returns the chance to block a strike that surpasses an entity's block defense.
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
            average += self.block_chance(attacker.fighter.active_weapon.item.equipment.attack_type, dmg)
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

    # def attempt_dodge(self):
    #     results = []
    #     exertion = self.defense * 2
    #     if self.stamina >= exertion:
    #         #results.append({'dodge_direction':(dx,dy)})
    #         results.append(self.exert(exertion, 'dodge'))
    #     else:
    #         results.append({'message':Message('PLACEHOLDER: Stamina too low to dodge!')})
    #     return results

    def death(self, game):

        ent = self.owner

        if game.debug['invin'] and ent.is_player:
            self.hp = self.max_hp
            return Message(f'Invincibility enabled')

        # Strip ent of components and set it as a corpse
        x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = colors.corpse
        ent.bg_color = colors.black
        ent.render_order = RenderOrder.CORPSE
        ent.blocks[BlockLevel.WALK] = False
        ent.blocks[BlockLevel.FLOOR] = False
        ent.ai = None
        if not self.owner.is_player:
            ent.fighter = None
        #ent.name = f'{ent.name.title()} remains'

        # Create gibs
        # TODO Consider force of impact (amount of damage done beyond 0 hp?) to vary spread
        game.map.tiles[(x, y)].gib()
        for i in range(1, randint(3, 5)):
            c_x, c_y = (randint(x - 1, x + 1), randint(y - 1, y + 1))
            game.map.tiles[(c_x, c_y)].gib()
            if not game.map.tiles[(c_x,c_y)].blocked and randint(0, 100) > 85:
                game.map.tiles[(c_x, c_y)].gib('~')

        type = MessageType.GOOD if not ent.is_player else MessageType.BAD
        message = Message(f'{ent.address_with_color.title()} {ent.state_verb_present} dead!', type=type, category=MessageCategory.OBSERVATION)

        return message
