from random import randint, choice

import logging

from dataclasses import dataclass, field

from components.combat.fighter_util import DamagePercentage, AttributePercentage, get_gui_data, State, Surrounded, \
    Stance
from components.statistics import statistics_updater
from config_files import colors, cfg
from data.actor_data.act_status_mod import status_modifiers_data
from data.data_enums import Key, Mod, ItemType
from data.gui_data.gui_fighter import hpdmg_string_data, stadmg_string_data, sta_color_data, stadmg_color_data, \
    sta_string_data, hpdmg_color_data, hp_string_data, hp_color_data
from gameobjects.block_level import BlockLevel
from gameobjects.util_functions import entity_at_pos, line_between_pos
from gui.messages import Message as M, MessageType, MessageCategory
from rendering.render_animations import animate_projectile, animate_move_line
from rendering.render_order import RenderOrder

@dataclass
class Fighter:
    __hp:int
    __stamina:int
    base_av:int
    base_strength:int
    __base_vision:int
    __default_effects:dict = field(default_factory=dict)
    owner = None  # owner is set by the Entity initializing the component

    def __post_init__(self):
        self.active_weapon = None
        self.max_hp = self.__hp
        self.max_stamina = self.__stamina
        self.surrounded = Surrounded.FREE
        self.stances = {
            Stance.BLOCKING: False,
            Stance.DASHING: False
        }
        self.effects = {
            State.DAZED: False,
            State.STUNNED: False,
            State.ENTANGLED: False,
            State.CONFUSED: False,
            State.IMMOBILE: False
        }
        for key in self.effects.keys():
            self.effects[key] = self.__default_effects.get(key, False)

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
    def is_blocking(self):
        return self.stances[Stance.BLOCKING]

    @property
    def is_dashing(self):
        return self.stances[Stance.DASHING]

    @property
    def strength(self):
        return self.base_strength

    @property
    def base_dmg_potential(self):
        """
        Attribute returns the entity's current damage potential (base + weapon)
        as tuple with the fighter's base str added.

        :return: (min/max damage)
        :rtype: tuple
        """
        if self.active_weapon is not None:
            return (self.strength + self.active_weapon.dmg_potential[0], self.strength + (self.active_weapon.dmg_potential[1]))
        return (self.strength, self.strength)

    @property
    def modded_dmg_potential(self):
        """
        Returns the fighter's modded damage potential, taking all possible modifiers into account.
        Only the average value between all modifiers is applied.

        :return: (min/max damage)
        :rtype: tuple
        """
        mod = 1
        modifiers = []

        # Moveset modifiers #
        if self.active_weapon is not None:
            modifiers.append(self.active_weapon.moveset.modifier(Mod.DMG_MULTIPL))

        # Status effects #
        for state, active in self.effects.items():
            if active:
                modifiers.append(status_modifiers_data[state].get('dmg_multipl',1))

        # Surrounded modifiers #
        modifiers.append(status_modifiers_data[self.surrounded].get('dmg_multipl',1))

        # Calculate average modifier
        if len(modifiers) > 0:
            mod = sum(modifiers)/len(modifiers)

        return (round(self.base_dmg_potential[0] * mod), round(self.base_dmg_potential[-1] * mod))

    @property
    def dmg_roll(self):
        """ Returns a random damage value, taking all possible modifiers into account """
        return randint(*self.modded_dmg_potential)

    @property
    def defense(self):
        total_defense = self.base_av
        if self.owner.paperdoll is not None:
            for e in self.owner.paperdoll.equipped_items:
                if e.armor_value is not None:
                    total_defense += e.armor_value

        return total_defense
    
    @property
    def modded_defense(self):
        mod = 1
        modifiers = []
        for state, active in self.effects.items():
            if active:
                modifiers.append(status_modifiers_data[state].get(Mod.AV_MULTIPL,1))

        modifiers.append(status_modifiers_data[self.surrounded].get(Mod.AV_MULTIPL,1))

        # Calculate average modifier
        if len(modifiers) > 0:
            mod = sum(modifiers) / len(modifiers)

        return round(self.defense * mod)

    @property
    def modded_block_def(self):
        block_def = self.shield.block_def
        if self.surrounded == Surrounded.THREATENED:
            block_def = round(block_def * 0.75)
        if self.surrounded == Surrounded.OVERWHELMED:
            block_def = 0
        return block_def

    @property
    def can_dash(self):
        exertion = self.defense * cfg.DASH_EXERT_MULTIPL
        return self.stamina >= exertion
    
    @property
    def vision(self):
        vision = self.__base_vision
        for e in self.owner.paperdoll.equipped_items:
            l_radius = vars(e.item.equipment).get(Key.L_RADIUS)
            # This extra step is required as l_radius value is set to None for all Equipment during data processing
            if l_radius is not None:
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
    def inactive_weapon(self):
        """
        :return: If two weapons are equipped, returns the inactive one, otherwise None.
        """
        if self.weapon_melee is not None and self.weapon_ranged is not None:
            if self.active_weapon == self.weapon_melee:
                return self.weapon_ranged
            else:
                return self.weapon_melee
        return None

    @property
    def shield(self):
        """
        :return: Equipment component (NOT entity itself) of currently equipped shield (or parrying weapon).
        """
        shield_ent = self.owner.paperdoll.shield_arm.shield  # TODO add check for 2nd hand after implementing dual wielding
        if shield_ent:
            return shield_ent.item.equipment
        else:
            return None

    def check_surrounded(self, game):
        nearby_enemies = self.owner.nearby_enemies_count(game)
        if nearby_enemies < 3:
            return Surrounded.FREE
        elif nearby_enemies < 5:
            return Surrounded.THREATENED
        else:
            return Surrounded.OVERWHELMED


    # GUI-related functions #
    # These all use current percentages of hp/stamina to pass a string or color on to the GUI.

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
        if self.owner.is_player:
            sta_dmg_string = self.stadmg_string(amount)
            col = self.stadmg_color(amount)
            message = M(f'{self.owner.possessive_colored.title()} {string} causes %{col}%{sta_dmg_string}%% exertion.',
                        category=MessageCategory.OBSERVATION, type=MessageType.COMBAT_INFO)
            return {'message': message}
        return {}

    def set_effect(self, state:State, value:bool=True, duration:int=0, msg=True):
        self.effects[state] = value
        if duration > 0: # If duration > 0, set a plan to disable the current presence in n turns
            self.owner.actionplan.add_to_queue(execute_in=duration,
                                               planned_function=self.set_effect,
                                               planned_function_args=(state, False))
        message = M(f'{self.owner.address_colored.title()} {self.owner.state_verb_present}{" no longer " if not value else " "}{state.name}!', category=MessageCategory.COMBAT)
        return [{'message': message}] if msg else []

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

    def attack_setup(self, target, game, dmg_mod_multipl:float=1, verb:str='hit', ignore_moveset:bool=False, draw_ranged_projectile:bool=True):
        results = []
        extra_attacks = []
        atk_exertion_divider = cfg.ATK_EXERT_DIVISOR
        daze_chance = 50 # chance to daze attacker on successful block # TODO dynamically calculated

        if self.active_weapon is not None: # if a weapon is equipped, check the type
            melee_attack = True if self.active_weapon.type == ItemType.MELEE_WEAPON else False
            ranged_attack = True if self.active_weapon.type == ItemType.RANGED_WEAPON else False
        else: # unarmed attack
            melee_attack = True
            ranged_attack = False
            ignore_moveset = True

        # Apply moveset modifers #
        if ignore_moveset:
            attack_power = choice(self.base_dmg_potential) * dmg_mod_multipl
            attack_exertion = attack_power / atk_exertion_divider
        else:
            if self.active_weapon is not None:
                move_results = self.active_weapon.moveset.execute(self.owner, target)
                verb = move_results.get('attack_verb', verb)
                extra_attacks = move_results.get('extra_attacks', [])

            attack_power = self.dmg_roll * dmg_mod_multipl
            attack_exertion = attack_power / atk_exertion_divider * self.active_weapon.moveset.exert_multipl
            self.active_weapon.moveset.cycle_moves()

        logging.debug(f'{self.owner.name} prepares to attack {target.name} with base damage {self.base_dmg_potential},'
                      f' (modded {self.modded_dmg_potential}) for a total power of {attack_power} and {attack_exertion}exert')

        # Make sure attacker has enough stamina #
        if self.stamina < attack_exertion:
            message = M(f'You are too exhaused to attack!', category=MessageCategory.COMBAT,
                              type=MessageType.ALERT)
            results.append({'message': message})
            logging.debug(f'Canceling {self}\'s attack: stamina of {self.stamina} too low.')
            return results

        # If the target is out of stamina, attack power is doubled #
        # TODO remove?
        if target.f.stamina <= 0 and melee_attack:
            logging.debug(f'{target} is out of stamina. Doubling {self}\'s atk_power to {attack_power}')
            attack_power *= 2

        # Ranged attack specific #
        if ranged_attack:
            logging.debug(f'{self.owner} is attempting ranged attack at {target}')
            if not self.owner.free_line_to_ent(target, game): # If the projectile's path to the intended target is obstructed
                pos_list = line_between_pos(*self.owner.pos, *target.pos) # Get a list of all pos between shooter and target
                # try:    # Get the first blocking entity from that list # TODO should be obsolete; kept to be sure
                obstacle = next(entity_at_pos(game.walk_blocking_ents, *pos) for pos in pos_list if entity_at_pos(game.walk_blocking_ents, *pos) is not None)
                logging.debug(f'{obstacle} is blocking direct los')
                if randint(0,1): # 50% chance that that entity is hit instead
                    # TODO chance will later be modified by skill level, attributes etc.
                    message = M(f'PLACEHOLDER: {self.owner.name} hits {obstacle.name} instead of {target.name}!',
                                      category=MessageCategory.COMBAT,
                                      type=MessageType.SYSTEM)
                    results.append({'message': message})
                    if obstacle.fighter is not None:
                        target = obstacle   # Intended target is switched for obstacle
                    else:
                        return results # If the obstacle can't be damaged, end the attack here
                # except:
                #     # TODO should be obsolete; kept to be sure
                #     message = M(f'PLACEHOLDER: {self.owner.name} hits a wall instead of {target.name}!',
                #                       category=MessageCategory.COMBAT,
                #                       type=MessageType.SYSTEM)
                #     results.append({'message': message})
                #     return results

            if draw_ranged_projectile:
                animate_projectile(*self.owner.pos,*target.pos,game, color=colors.beige) # TODO color and projectile can later be modified by weapon/ammo

        # Blocking #
        attack_blocked = False
        if target.f.is_blocking:
            attack_blocked = target.f.attempt_block(self, attack_power)

        if attack_blocked:
            # TODO should attacker also take sta damage?
            sta_dmg_multipl = self.active_weapon.moveset.modifier(Mod.BLOCK_STA_DMG_MULTIPL) # Some weapons afflict a higher stamina damage
            sta_dmg = round((attack_power / 2) * sta_dmg_multipl)
            logging.debug(f'{target.name} block exert multiplied by {sta_dmg_multipl} due to {self.owner.name} attack mod')
            results.append(target.f.exert(sta_dmg, 'block'))

            if melee_attack and randint(0,100) > daze_chance:
                if target.is_player:
                    message = M(f'{target.address_colored.title()} block the attack, dazing {self.owner.address_colored}!',
                                category=MessageCategory.COMBAT, type=MessageType.COMBAT_GOOD)
                else:
                    message = M(f'{self.owner.address_colored.title()} blocks your attack, dazing {target.owner.address_colored}!',
                                category=MessageCategory.COMBAT, type=MessageType.COMBAT_BAD)
                self.set_effect(State.DAZED, True, 1)
                results.append({'message': message})
        else:
            attack_string = self.owner.verb_declination(verb)
            results.extend(self.attack_execute(target, attack_power, attack_string))

        for attack_pos in extra_attacks:
            extra_target = entity_at_pos(game.npc_ents, *attack_pos)
            if extra_target:
                results.extend(self.attack_execute(extra_target, attack_power // 2, 'also hit')) # TODO currently flat half damage and can't be blocked; can be replaced with moveset-tailored multiplier

        self.exert(attack_exertion, 'attack')

        return results

    def attack_execute(self, target, power, attack_string):
        results = []

        damage = round(power - (target.f.modded_defense))
        deflect_exertion = power * cfg.DEFLECT_EXERT_MULTIPL

        if target == self.owner:
            target_string = 'itself' if not target.is_player else 'yourself'
        else:
            target_string = target.address_colored

        if damage > 0:
            msg_type = MessageType.COMBAT_BAD if target.is_player else MessageType.COMBAT_INFO
            atk_dmg_string = target.f.hpdmg_string(damage)
            col = target.f.hpdmg_color(damage)
            results.append({'message': M(
                f'{self.owner.address_colored.title()} {attack_string} {target_string}, {choice(hpdmg_string_data["verbs"])} %{col}%{atk_dmg_string}%% damage.', category=MessageCategory.COMBAT, type=msg_type)})
            results.extend(target.f.take_damage(damage))

            # STATISTICS
            self.owner.statistics.dmg_done += damage
            if target.f.hp <= 0:
                self.owner.statistics.killed += [target.name]

        else:
            msg_type = MessageType.COMBAT_BAD if not target.is_player else MessageType.COMBAT_GOOD
            results.append(
                {'message': M(f'{self.owner.address_colored.title()} {attack_string} {target_string} but can not penetrate armor.', category=MessageCategory.COMBAT, type=msg_type)})
            results.append(target.f.exert(deflect_exertion, 'deflection'))

        logging.debug(
            f'{self.owner.name.title()} attacks {target.name.title()} with {power} power against {target.f.defense} defense for {damage} damage. Target has {target.f.stamina} stamina left.)')
        return results

    def tackle(self, target, game, multipl:float=0.5, duration=2):
        result = []
        t_hp = target.f.hp
        result.extend(self.attack_setup(target, game, dmg_mod_multipl=multipl, verb='tackle', ignore_moveset=True))
        if target.f.hp < t_hp: # if target lost hp, daze it
            result.extend(target.f.set_effect(State.DAZED, True, duration))
        return result

    #############################
    # DEFENSE RELATED FUNCTIONS #
    #############################

    def toggle_blocking(self):
        results = []

        if self.is_blocking:
            results.append({'message': M(f'{self.owner.address_colored.title()} stop blocking.', type=MessageType.COMBAT_INFO)})
            self.stances[Stance.BLOCKING] = False
        elif self.shield:
            results.append({'message': M(f'{self.owner.address_colored.title()} ready your {self.shield.owner.owner.name_colored}.', type=MessageType.COMBAT_INFO)})
            self.stances[Stance.BLOCKING] = True
        else:
            results.append({'message': M(f'{self.owner.address_colored.title()} need a shield to block.', type=MessageType.COMBAT_INFO)})

        return results


    def toggle_dashing(self):
        results = []

        if self.is_dashing:
            results.append({'message': M(f'{self.owner.address_colored.title()} stop dashing.', type=MessageType.COMBAT_INFO)})
            self.stances[Stance.DASHING] = False
        else:
            results.append({'message': M(f'{self.owner.address_colored.title()} prepare to dash.', type=MessageType.COMBAT_INFO)})
            self.stances[Stance.DASHING] = True

        return results


    def dash(self, dx, dy, game, distance:int=2):
        results = []

        if self.can_dash:
                moved = animate_move_line(self.owner, dx, dy, distance, game, anim_delay=0.05)
                results.append(self.exert(self.defense * cfg.DASH_EXERT_MULTIPL, 'dash'))
                if moved is not True and not isinstance(moved, bool): # If dash was stopped by another entity, proceed to tackle
                    target = moved
                    if target.f is not None:
                        results.extend(self.tackle(target, game))
        else:
            results.append({'message': M(f'{self.owner.address_colored.title()} are too exhausted!', type=MessageType.COMBAT_BAD)})

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
            chance = self.block_chance(attacker.active_weapon, damage)
            if chance > 0 and chance >= randint(0,100):
                return True
        return False


    def block_chance(self, attacking_weapon, damage):
        """
        Returns the chance to block a strike that surpasses an entity's block defense.
        It is possible to block up to the double of maximum block defense.
        """
        if self.shield is None:
            return 0
        block_def = self.shield.block_def
        #mod = wp_attacktypes_data[attack_type].get(Key.BLOCK_DEF_MULTIP,1)
        mod = attacking_weapon.moveset.modifier(Mod.BLOCK_DEF_MULTIPL)
        block_def = round(block_def * mod)
        logging.debug(f'{self.owner.name} block def. multiplied by {mod} due to {attacking_weapon}')

        if block_def > 0:
            return 101 - ((damage - block_def) / block_def * 100)
        else:
            return 0

    def average_chance_to_block(self, attacker, debug=False):
        """
        Utility function for debug information and an entities description window.
        """
        average = 0
        dmg_range = attacker.f.base_dmg_potential
        for dmg in dmg_range:
            average += self.block_chance(attacker.f.active_weapon, dmg)
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

    def death(self, game):

        ent = self.owner
        ent_old_color = ent.color
        blood = colors.blood_red if ent.color_blood is None else ent.color_blood

        if game.debug['invincibility'] and ent.is_player:
            self.hp = self.max_hp
            return M(f'Invincibility enabled')

        # Strip ent of components and set it as a corpse
        # x, y = ent.x, ent.y
        ent.char = '%'
        ent.color = blood
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
        game.map.gib_area(ent.x, ent.y, randint(3,5), blood, chunks=True)

        type = MessageType.GOOD if not ent.is_player else MessageType.BAD
        message = M(f'The %{ent_old_color}%{ent.name}%% {ent.state_verb_present} dead!', type=type, category=MessageCategory.OBSERVATION)

        return message
