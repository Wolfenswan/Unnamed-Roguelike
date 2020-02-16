import logging
from functools import wraps
from random import choice
from typing import Optional, Union, List, Tuple

from dataclasses import dataclass, field
from tcod import Color

from config_files import colors

from components.skills.skillList import SkillList
from components.actionplan import Actionplan
from components.combat.fighter_util import State, Stance
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.inventory.paperdoll import Paperdoll
from components.items.item import Item
from components.statistics import Statistics
from data.actor_data.act_status_mod import status_modifiers_data
from data.data_enums import GenericType, MonsterType, ItemType, Material, BodyType, Mod
from data.gui_data.gui_entity import bodytype_name_data
from data.gui_data.material_strings import material_name_data
from data.gui_data.gui_fighter import effects_descr_data
from game import Game
from gameobjects.util_functions import entity_at_pos, free_line_between_pos, distance_between_pos
from map.directions_util import direction_between_pos, DIRECTIONS_CIRCLE
from map.game_map import GameMap
from rendering.render_order import RenderOrder

@dataclass
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    x : int
    y : int
    char : str
    color : Color
    name : str
    descr : str = ''
    type : Union[GenericType, ItemType, MonsterType] = field(default=GenericType.DEFAULT)
    blocks : dict = field(default_factory=dict)
    render_order : RenderOrder = field(default=RenderOrder.NONE)

    material: Optional[Material] = None
    bodytype: Optional[BodyType] = None

    fighter : Optional = None
    ai: Optional = None
    skills: Optional[SkillList] = None
    item: Optional[Item] = None
    inventory: Optional[Inventory] = None
    paperdoll: Optional[Paperdoll] = None
    qu_inventory: Optional[Inventory] = None
    architecture: Optional[Architecture] = None

    is_player: Optional[bool] = False
    color_bg : Optional[Color] = None
    color_blood: Optional[Color] = None
    every_turn_start : Optional[list] = field(default_factory=list)
    every_turn_end : Optional[list] = field(default_factory=list)

    def __post_init__(self):
        self.actionplan = Actionplan()
        self.statistics = Statistics()

        if self.fighter is not None:
            self.f.owner = self

        if self.ai is not None:
            self.ai.owner = self
            if self.ai.behavior is not None:
                self.ai.behavior.owner = self

        if self.item is not None:
            self.item.owner = self

        if self.inventory is not None:
            self.paperdoll = Paperdoll()
            self.qu_inventory = Inventory(capacity=0)
            self.inventory.owner = self
            self.paperdoll.owner = self
            self.qu_inventory.owner = self

        if self.architecture is not None:
            self.architecture.owner = self

        if self.skills is not None:
            self.skills.owner = self
            for skill in self.skills:
                skill.owner = self

        self.actionplan.owner = self
        self.statistics.owner = self

    def __repr__(self):
        string = f'{self.name}:{id(self)}'
        if self.pos != (0, 0):
            string += f'({self.pos})'
        return string

    def __eq__(self, other): # For some reason entities from the same data set but with different ids are considered equal by default
        return id(self) == id(other)

    ###############################
    # ATTRIBUTE RELATED FUNCTIONS #
    ###############################

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, new_pos:Tuple[int,int]):
        self.x = new_pos[0]
        self.y = new_pos[1]

    @property
    def full_name(self):
        """
        :return: Entity's name + relevant adjectives.
        :rtype: str
        """
        full_name = self.name
        if self.material:
            full_name = f'{material_name_data[self.material]} {self.name}'

        if self.bodytype and self.bodytype != BodyType.NORMAL:
            full_name = f'{bodytype_name_data[self.bodytype]} {self.name}'

        if self.item:
            if self.item.prefix:
                full_name = f'{self.item.prefix} {full_name}'
            if self.item.suffix:
                full_name += f' {self.item.suffix}'

        if self.fighter and self.f.hp <= 0:
            full_name += ' remains'

        # if self.architecture and self.inventory and self.inventory.is_empty:
        #     full_name += '(e)'

        # TODO doors (open & unlocked)

        return full_name.title()

    def extended_descr(self, game):
        """

        :param game: global game entity
        :type game: Game
        :return: Entity's formatted description, including dynamic information depending on player stats.
        :rtype: str
        """
        extend_descr = self.descr
        col = 'dark_crimson' # TODO All colors are placeholders
        if self.fighter is not None and self.active_weapon is not None:
            # if self.f.active_weapon: # TODO add another way to indicate special features of a creatures attack
            #     extend_descr += f'\n\nIt attacks with %{col}%{self.f.active_weapon.item.equipment.attack_type.name.lower()}%% strikes.'

            if game.player.f.shield:
                extend_descr += f'\n\nBlocking its attacks is\n %{col}%{game.player.f.average_chance_to_block(self)}%%.'

            for effect, active in self.f.effects.items():
                if active and effects_descr_data.get(effect, None) is not None:
                    extend_descr += f'\n\n{self.pronoun.title()} {self.state_verb_present} {effects_descr_data[effect]}'

        if self.item:
            extend_descr += self.item.attr_list

        if game.debug['detailed_ent_info']:
            if self.fighter is not None:
                extend_descr += f'\n\nhp:{self.f.hp}/{self.f.max_hp}'
                extend_descr += f'\n\nsta:{self.f.stamina}/{self.f.max_stamina}'
                extend_descr += f'\nav:{self.f.defense} (modded:{self.f.modded_defense})'
                extend_descr += f'\ndmg:{self.f.base_dmg_potential} (modded:{self.f.modded_dmg_potential})'
                if self.active_weapon is not None:
                    extend_descr += f'\n\nwp:{self.f.active_weapon.full_name}'
                    extend_descr += f'\nYour ctb:{game.player.f.average_chance_to_block(self, debug=True)}'
            if self.architecture:
                ext1 = self.architecture.on_interaction.__name__ if self.architecture.on_interaction else None
                ext2 = self.architecture.on_collision.__name__ if self.architecture.on_collision else None
                extend_descr += f'\n\ninteract:{ext1}, collision:{ext2}'

        return extend_descr

    def is_visible(self, fov_map):
        return fov_map.fov[self.y, self.x]

    @property
    def is_corpse(self):
        return self.f.hp <= 0 if self.fighter else False

    @property
    def can_move(self):
        if self.fighter:
            for state, active in self.effects.items():
                if active and status_modifiers_data[state].get(Mod.CAN_MOVE, True) is False:
                    return False
            else: # for...else triggers if the for loop finished without breaking
                return True
        else:
            return True

    @property
    def can_attack(self):
        if self.fighter:
            for state, active in self.effects.items():
                if active and status_modifiers_data[state].get(Mod.CAN_ATTACK, True) is False:
                    return False
            else:   # for...else applies if the for loop finished without breaking
                return True
        else:
            return False

    def in_combat(self, game): # NOTE: Only relevant for player at the moment.
        enemies = game.npc_ents
        visible_enemies = self.visible_enemies(enemies, game.fov_map)
        if len(visible_enemies) > 0:
            return True
        else:
            return False

    #########################################################
    # CONVENIENCE PROPERTIES TO ACCESS COMPONENT ATTRIBUTES #
    #########################################################

    @property
    def active_weapon(self):
        return self.f.active_weapon if self.fighter is not None else None

    @property
    def active_weapon_is_melee(self):
        if self.active_weapon is None:
            return False
        return self.active_weapon.type == ItemType.RANGED_WEAPON

    @property
    def active_weapon_is_ranged(self):
        if self.active_weapon is None:
            return False
        return self.active_weapon.type == ItemType.RANGED_WEAPON

    # @property
    # def attack_type(self):
    #     return self.item.equipment.attack_type if self.item is not None and self.item.equipment is not None else None

    @property
    def dmg_potential(self):
        return self.item.equipment.dmg_potential if self.item is not None and self.item.equipment is not None else None

    @property
    def armor_value(self):
        return self.item.equipment.av if self.item is not None and self.item.equipment is not None else None

    @property
    def attack_range(self):
        return self.item.equipment.attack_range if self.item is not None and self.item.equipment is not None else None

    @property
    def moveset(self):
        return self.item.equipment.moveset if self.item is not None and self.item.equipment is not None else None

    @property
    def effects(self):
        return self.f.effects if self.fighter is not None else None

    def is_active_weapon(self,ent):
        return self == ent.f.active_weapon

    ####################
    # ACTION FUNCTIONS #
    ####################

    def move(self, dx, dy, absolute=False):
        # Move the entity i
        if not absolute:
            self.x += dx
            self.y += dy
        else:
            self.x, self.y = dx, dy

    def try_move(self, dx:int, dy:int, game:Game, ignore_entities:bool=False, ignore_walls:bool= False, absolute:bool=False):
        """
        Attempts to move the entity in the given direction or to the given coordinates.
        Returns True on successful move.
        Returns False if wall blocks movement or entity is unable to move due to effects.
        Returns Entity if entity blocks movement.

        :param dx:
        :type dx: int
        :param dy:
        :type dy: int
        :param game:
        :type game: Game
        :param ignore_entities: Whether to ignore blocking entities when checking for movement.
        :type ignore_entities: bool
        :param ignore_walls: Whether to ignore walls when checking for movement.
        :type ignore_walls: bool
        :param absolute: Whether dx&dy denote directions or a x/y coordinates on the grid
        :type absolute: bool
        :return:
        :rtype: bool
        """
        if not self.can_move:
            return False

        if not absolute:
            dest_x, dest_y = self.x + dx, self.y + dy
        else:
            dest_x, dest_y = dx, dy

        if game.map.is_wall(dest_x, dest_y) and not ignore_walls:
            return False

        blocked = entity_at_pos(game.walk_blocking_ents, dest_x, dest_y)
        if blocked and not ignore_entities:
            return blocked

        self.move(dx, dy, absolute=absolute)
        return True

    def proc_every_turn(self, game, start=True):
        """
        Things that should every proper turn (after player has done an action that prompts an enemy turn.)
        """
        if start:
            self.statistics.reset_turn()
            for event in self.every_turn_start:
                eval(event)
        else:
            if self.is_player:
                self.actionplan.process_queue()
                # TODO Placeholder for proper stamina management (currently flat 1% recovered)
                if not self.in_combat(game) and not self.f.sta_full and not self.f.stances.get(Stance.DASHING,False):
                    self.f.recover(self.f.max_stamina / 100)
            for event in self.every_turn_end:
                eval(event)

    #####################
    # UTILITY FUNCTIONS #
    #####################

    def set_random_color(self, colors):
        self.color = choice(colors)

    def distance_to_pos(self, x, y):
        return distance_between_pos(*self.pos, x, y)

    def distance_to_ent(self, other):
        return self.distance_to_pos(other.x, other.y)

    def free_line_to_ent(self, other, game:Game):
        return free_line_between_pos(*self.pos, *other.pos, game)

    def direction_to_pos(self, x, y):
        return direction_between_pos(*self.pos, x, y)

    def direction_to_ent(self, other):
       return self.direction_to_pos(*other.pos)

    def same_pos_as(self, other_ent):
        return self.pos == other_ent.pos

    def entities_in_distance(self, entities:List, dist:float=1.5):
        """ returns nearby entities in given distance """
        entities_in_range = [ent for ent in entities if ent != self and self.distance_to_ent(ent) <= dist]
        return entities_in_range

    def enemies_in_distance(self, hostile_entities:List, dist:float=1.5): # NOTE: Only relevant for player at the moment.
        """ returns nearby monsters in given distance. Note: dist=1.5 covers all tiles right next to the player. """
        ents = self.entities_in_distance(hostile_entities, dist=dist)
        ents = [ent for ent in ents if not ent.is_corpse]
        return ents

    def nearest_entity(self, entities:List, max_dist:float=5):
        entities_in_range = self.entities_in_distance(entities, max_dist)
        if entities_in_range:
            return sorted(entities_in_range, key=lambda ent: ent.distance_to_ent(self))[0]
        return None

    # def nearest_enemy(self, hostile_entities:List, fov_map):
    #     return next(self.visible_enemies(hostile_entities, fov_map))

    def surrounding_enemies(self, hostile_entities:List):
        ents = self.entities_in_distance(hostile_entities, dist=1.5)
        return ents

    def visible_enemies(self, hostile_entities, fov_map): # NOTE: Only relevant for player at the moment.
        enemies_in_distance = self.enemies_in_distance(hostile_entities, dist=self.f.vision)
        visible_enemies = [ent for ent in enemies_in_distance if ent.is_visible(fov_map)]
        return visible_enemies

    def nearby_enemies_count(self,game):
        return len(self.surrounding_enemies(game.npc_ents))

    ########################
    # COMPONENT SHORTHANDS #
    ########################

    @property
    def f(self):
        return self.fighter

    @property
    def i(self):
        return self.item

    @property
    def inv(self):
        return self.inventory

    @property
    def qu(self):
        return self.qu_inventory

    ################
    # GUI HELPERS #
    ###############

    @property
    def name_colored(self):
        return f'%{self.color}%{self.name.title()}%%'

    @property
    def pronoun(self):
        return 'it' if not self.is_player else 'you'

    @property
    def address(self):
        return f'the {self.name}' if not self.is_player else 'you'

    @property
    def address_colored(self):
        return f'the %{self.color}%{self.name}%%' if not self.is_player else f'%{self.color}%you%%'

    @property
    def possessive(self):
        return f'{self.address}\'s' if not self.is_player else 'your'

    @property
    def possessive_colored(self):
        return f'{self.address}\'s' if not self.is_player else f'%{self.color}%your%%'

    @property
    def state_verb_present(self):
        return self.verb_declination('is')

    @property
    def state_verb_past(self):
        return self.verb_declination('was')

    def verb_declination(self, verb):
        if verb == 'is':
            if self.is_player:
                verb = 'are'
        elif verb == 'was':
            if self.is_player:
                verb = 'were'
        elif not self.is_player:
            if verb[-1] == 'o' or verb[-2:] in ['sh', 'ch', 'tch', 'x', 'z', 'ss'] or (
                    verb[-1] == 'y' and not verb[-2] in ['a', 'e', 'i', 'o', 'u']):
                verb += 'es'
            else:
                verb += 's'
        return verb