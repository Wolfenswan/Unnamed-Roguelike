import math
from enum import Enum, auto

import tcod

from components.actionplan import Actionplan
from components.actors.status_modifiers import Presence
from components.inventory.inventory import Inventory
from components.inventory.paperdoll import Paperdoll
from config_files import colors
from data.data_types import BodyType
from data.gui_data.gui_entity import bodytype_name_data
from data.gui_data.material_strings import material_name_data
from gameobjects.util_functions import entity_at_pos
from rendering.render_order import RenderOrder


class EntityStates(Enum):
    ENTITY_ACTIVE = auto()
    ENTITY_STUNNED = auto()
    ENTITY_WAITING = auto()


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, descr=None, type=None,
                 material=None, bodytype=None,
                 is_player=False, is_corpse=False, blocks=None, render_order=RenderOrder.CORPSE,
                 fighter=None, ai=None, skills=None, item=None, inventory=None, architecture=None):
        self.state = EntityStates.ENTITY_ACTIVE
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.color_bg = None
        self.name = name
        self.descr = descr
        self.type = type
        self.material = material
        self.bodytype = bodytype
        self.is_player = is_player
        self.is_corpse = is_corpse
        self.blocks = blocks
        if not self.blocks:
            self.blocks = {}
        self.render_order = render_order

        # Components #
        self.fighter = fighter
        self.ai = ai
        self.actionplan = Actionplan()
        self.item = item
        self.inventory = inventory
        if self.inventory:
            self.paperdoll = Paperdoll()
            self.qu_inventory = Inventory(capacity = 0)
        self.skills = skills  # dictionary
        self.architecture = architecture
        self.set_ownership() # Sets ownership for all components
    
    def set_ownership(self):
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self
            self.paperdoll.owner = self
            self.qu_inventory.owner = self

        if self.architecture:
            self.architecture.owner = self

        if self.skills is not None:
            for skill in self.skills.values():
                skill.owner = self

        self.actionplan.owner = self

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
    def state_verb(self):
        return 'is' if not self.is_player else 'are'

    def extended_descr(self, game):
        extend_descr = []
        # TODO All colors are WIP
        if self.fighter and self.fighter.weapon:
            extend_descr += [f'It attacks with %dark_crimson%{self.fighter.weapon.attack_type.name.lower()}%% strikes.']

        if self.fighter and game.player.fighter.shield:
            extend_descr += [f'Blocking its attacks will be %dark_crimson%{game.player.fighter.average_chance_to_block(self)}%%.']

        if self.fighter and self.fighter.presence[Presence.DAZED]:
            extend_descr += [f'{self.pronoun.title()} {self.state_verb} %yellow%dazed%% and slightly confused.']

        if self.fighter and self.fighter.presence[Presence.STUNNED]:
            extend_descr += [f'{self.pronoun.title()} {self.state_verb} %yellow%stunned%% and unable to attack.']

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


    def available_skills(self, game):
        available_skills = [skill for skill in self.skills.values() if skill.is_available(game)]
        return available_skills

    def cooldown_skills(self, reset=False):
        for skill in self.skills.values():
            skill.cooldown_skill(reset=reset)

    def is_visible(self, fov_map):
        return tcod.map_is_in_fov(fov_map, self.x, self.y)

    def in_combat(self, game): # NOTE: Only relevant for player at the moment.
        enemies = game.npc_ents
        visible_enemies = self.visible_enemies(enemies, game.fov_map)
        if len(visible_enemies) > 0:
            return True
        else:
            return False

    def proc_every_turn(self, last_player_action, game):
        """
        Things that should every proper turn (after player has done an action that prompts an enemy turn.)
        """
        if self.is_player:
            # TODO Placeholder for proper stamina managment
            if not self.in_combat(game) and not last_player_action.get('dodge'):
                self.fighter.recover(self.fighter.max_stamina / 100)

    ####################
    # ACTION FUNCTIONS #
    ####################

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def try_move(self, dx, dy, game, ignore_entities=False, ignore_walls = False):
        """
        Attempts to move the entity in the given direction.
        If the direction is blocked by another entity, the blocking entity is returned.
        If the direction is non-walkable, False is returned

        """
        dest_x, dest_y = self.x + dx, self.y + dy
        if not game.map.is_wall(dest_x, dest_y) or ignore_walls:
            blocked = entity_at_pos(game.blocking_ents, dest_x, dest_y)
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
                    break

    #####################
    # UTILITY FUNCTIONS #
    #####################

    def distance_to_pos(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to_ent(self, other):
        return self.distance_to_pos(other.x, other.y)

    def direction_to_pos(self, x, y):
        dx, dy = 0, 0
        x_plane = x - self.x
        y_plane = y - self.y

        if x_plane > 0:
            dx = 1
        elif x_plane < 0:
            dx = -1

        if y_plane > 0:
            dy = 1
        elif y_plane < 0:
            dy = -1

        return dx, dy

    def direction_to_ent(self, other):
        dx, dy = 0, 0
        x_plane = other.x - self.x
        y_plane = other.y - self.y

        if x_plane > 0:
            dx = 1
        elif x_plane < 0:
            dx = -1

        if y_plane > 0:
            dy = 1
        elif y_plane < 0:
            dy = -1

        return dx, dy

    def same_pos_as(self, other_ent):
        return self.pos == other_ent.pos

    def get_nearby_entities(self, game, ai_only=False, dist=1.5, filter_player = True):
        """ returns nearby entitis in given distance """
        # TODO check perfomance, double check if works as expected
        entities_in_range = [ent for ent in game.entities if ent.distance_to_ent(self) <= dist and ent != self and (ai_only and ent.ai is not None) and (filter_player and ent.is_player == False)]
        return entities_in_range

    def enemies_in_distance(self, hostile_entities, dist=1.5): # NOTE: Only relevant for player at the moment.
        """ returns nearby monsters in given distance. Note: dist=1.5 covers all tiles right next to the player. """
        enemies_in_distance = [ent for ent in hostile_entities if self.distance_to_ent(ent) <= dist and ent != self and ent.fighter is not None and not ent.is_corpse]
        return enemies_in_distance

    def visible_enemies(self, hostile_entities, fov_map): # NOTE: Only relevant for player at the moment.
        enemies_in_distance = self.enemies_in_distance(hostile_entities, dist=self.fighter.vision)
        visible_enemies = [ent for ent in enemies_in_distance if ent.is_visible(fov_map) and ent != self and ent.fighter is not None and not ent.is_corpse]
        return visible_enemies
