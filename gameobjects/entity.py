import logging
import math
from random import choice
from typing import Optional, Union, List

import tcod
from dataclasses import dataclass, field

from components.AI.baseAI import BaseAI
from components.actors.skills import Skills
from components.actionplan import Actionplan
from components.actors.fighter import Fighter
from components.actors.status_modifiers import Presence
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.inventory.paperdoll import Paperdoll
from components.items.item import Item
from components.statistics import Statistics
from config_files import colors
from data.data_types import BodyType, Material, GenericType, MonsterType, ItemType
from data.gui_data.gui_entity import bodytype_name_data
from data.gui_data.material_strings import material_name_data
from debug.timer import debug_timer
from game import Game
from gameobjects.util_functions import entity_at_pos
from map.directions_util import direction_between_pos
from rendering.render_order import RenderOrder

@dataclass
class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    x : int
    y : int
    char : str
    color : tuple
    name : str
    descr : str = ''
    type : Union[GenericType, ItemType, MonsterType] = field(default=GenericType.DEFAULT)
    blocks : dict = field(default_factory=dict)
    render_order : RenderOrder = field(default=RenderOrder.NONE)

    material: Optional[Material] = None
    bodytype: Optional[BodyType] = None

    fighter : Optional[Fighter] = None
    ai: Optional[BaseAI] = None
    skills: Optional[Skills] = None
    item: Optional[Item] = None
    inventory: Optional[Inventory] = None
    paperdoll = None
    qu_inventory = None
    architecture: Optional[Architecture] = None

    is_player: bool = False
    color_bg : Optional[tuple] = None
    every_turn_start : Optional[list] = field(default_factory=list)
    every_turn_end : Optional[list] = field(default_factory=list)

    def __post_init__(self):
        self.actionplan = Actionplan()
        self.statistics = Statistics()

        if self.fighter is not None:
            self.fighter.owner = self

        if self.ai is not None:
            self.ai.owner = self

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
        return f'{self.name} ({id(self)}) at {self.pos}'

    ###############################
    # ATTRIBUTE RELATED FUNCTIONS #
    ###############################

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def full_name(self):
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

        if self.architecture and self.inventory.capacity > 0:
            if self.inventory.is_empty:
                full_name += ' (empty)'

        if self.fighter and self.fighter.hp <= 0:
            full_name += ' remains'

        # TODO doors (open & unlocked)

        return full_name.title()

    @property
    def pronoun(self):
        return 'it' if not self.is_player else 'you'

    @property
    def address(self):
        return f'the {self.name}' if not self.is_player else 'you'

    @property
    def state_verb_present(self):
        return 'is' if not self.is_player else 'are'

    @property
    def state_verb_past(self):
        return 'was' if not self.is_player else 'were'

    def extended_descr(self, game):
        extend_descr = []
        # TODO All colors are WIP
        if self.fighter and self.fighter.weapon:
            extend_descr += [f'It attacks with %dark_crimson%{self.fighter.weapon.attack_type.name.lower()}%% strikes.']

        if self.fighter and game.player.fighter.shield:
            extend_descr += [f'Blocking its attacks will be %dark_crimson%{game.player.fighter.average_chance_to_block(self)}%%.']

        if self.fighter and self.fighter.presence[Presence.DAZED]:
            extend_descr += [f'{self.pronoun.title()} {self.state_verb_present} %yellow%dazed%% and slightly confused.']

        if self.fighter and self.fighter.presence[Presence.STUNNED]:
            extend_descr += [f'{self.pronoun.title()} {self.state_verb_present} %yellow%stunned%% and unable to attack.']

        if game.debug['ent_info']:
            if self.fighter:
                extend_descr += [f'hp:{self.fighter.hp}/{self.fighter.max_hp}',
                                f'av:{self.fighter.defense} (modded:{self.fighter.modded_defense})',
                                f'dmg:{self.fighter.base_dmg_potential} (modded:{self.fighter.modded_dmg_potential})',
                                f'Your ctb:{game.player.fighter.average_chance_to_block(self, debug=True)}']
            if self.fighter.weapon:
                extend_descr += [f'wp:{self.fighter.weapon.full_name}']
            if self.architecture:
                ext1 = self.architecture.on_interaction.__name__ if self.architecture.on_interaction else None
                ext2 = self.architecture.on_collision.__name__ if self.architecture.on_collision else None
                extend_descr += [f'interact:{ext1}', f'collision:{ext2}']

        return extend_descr

    def is_visible(self, fov_map):
        return tcod.map_is_in_fov(fov_map, self.x, self.y)

    @property
    def is_corpse(self):
        return self.fighter.hp <= 0 if self.fighter else False

    def in_combat(self, game): # NOTE: Only relevant for player at the moment.
        enemies = game.npc_ents
        visible_enemies = self.visible_enemies(enemies, game.fov_map)
        if len(visible_enemies) > 0:
            return True
        else:
            return False

    ####################
    # ACTION FUNCTIONS #
    ####################

    def move(self, dx, dy):
        # Move the entity by a given amount
        logging.debug(f'{self} is moving.')
        self.x += dx
        self.y += dy
        logging.debug(f'{self} has moved.')

    def try_move(self, dx, dy, game, ignore_entities=False, ignore_walls = False):
        """
        Attempts to move the entity in the given direction.
        If the direction is blocked by another entity, the blocking entity is returned.
        If the direction is non-walkable, False is returned

        """
        dest_x, dest_y = self.x + dx, self.y + dy
        if not game.map.is_wall(dest_x, dest_y) or ignore_walls:
            blocked = entity_at_pos(game.walk_blocking_ents, dest_x, dest_y)
            if blocked and not ignore_entities:
                return blocked
            else:
                self.move(dx, dy)
        else:
            return False

    def move_away_from(self, target, game):
        """ Move Entity away from intended target """

        # loop through available directions and pick the first that is at least one square from the player
        # loop does not check for walls, so an entity can back up into walls (and thus fail/be cornered)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                flee_pos = (self.x + dx, self.y + dy)
                distance = target.distance_to_pos(*flee_pos)
                if distance > 1.5:
                    self.try_move(dx, dy, game)
                    return

    def proc_every_turn(self, last_player_action, game, start=True):
        """
        Things that should every proper turn (after player has done an action that prompts an enemy turn.)
        """
        if start:
            self.statistics.reset_turn()
            for event in self.every_turn_start:
                eval(event)
        else:
            if self.is_player:
                # TODO Placeholder for proper stamina managment
                if not self.in_combat(game) and not self.fighter.sta_full and not last_player_action.get('dodge'):
                    self.fighter.recover(self.fighter.max_stamina / 100)
            for event in self.every_turn_end:
                eval(event)

    #####################
    # UTILITY FUNCTIONS #
    #####################

    def set_random_color(self, colors):
        self.color = choice(colors)

    def distance_to_pos(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to_ent(self, other):
        return self.distance_to_pos(other.x, other.y)

    def direction_to_pos(self, x, y):
        return direction_between_pos(*self.pos, x, y)

    def direction_to_ent(self, other):
       return self.direction_to_pos(*other.pos)

    def same_pos_as(self, other_ent):
        return self.pos == other_ent.pos

    def entities_in_distance(self, entities:[List], dist:float=1.5):
        """ returns nearby entities in given distance """
        entities_in_range = [ent for ent in entities if ent != self and self.distance_to_ent(ent) <= dist]
        logging.debug(f'Nearby : {entities_in_range}')
        return entities_in_range

    def enemies_in_distance(self, hostile_entities:List, dist:float=1.5): # NOTE: Only relevant for player at the moment.
        """ returns nearby monsters in given distance. Note: dist=1.5 covers all tiles right next to the player. """
        ents = self.entities_in_distance(hostile_entities, dist=dist)
        ents = [ent for ent in ents if not ent.is_corpse]
        return ents

    def surrounding_enemies(self, hostile_entities:List):
        ents = self.entities_in_distance(hostile_entities, dist=1.5)
        return ents

    def visible_enemies(self, hostile_entities, fov_map): # NOTE: Only relevant for player at the moment.
        enemies_in_distance = self.enemies_in_distance(hostile_entities, dist=self.fighter.vision)
        visible_enemies = [ent for ent in enemies_in_distance if ent.is_visible(fov_map)]
        return visible_enemies
