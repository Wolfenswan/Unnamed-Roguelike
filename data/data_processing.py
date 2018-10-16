import logging
from random import choice, randint
from typing import Dict

from components.AI.baseAI import BaseAI
from components.AI.behavior.simple import Simple
from components.actors.fighter import Fighter
from components.skills.skillList import SkillList
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.items.equipment import Equipment
from components.items.item import Item
from components.items.moveset import Moveset
from components.items.useable import Useable
from config_files import colors
from data.actor_data.test_spawns import spawn_data
from data.architecture_data.arch_static import arch_static_data
from data.architecture_data.arch_containers import arch_containers_data
from data.item_data.use_bombs import use_bombs_data
from data.item_data.wp_creatures import wp_creature_data
from data.gui_data.craft_strings import craft_descr_data
from data.actor_data.act_bodytypes import bodytype_data
from data.shared_data.quality_mod import qual_cond_data, qual_craft_data
from data.data_types import GenericType, Condition, RarityType, BodyType, Material, Craftsmanship
from data.shared_data.material_mod import item_material_data
from data.item_data.test_equipment import test_equipment_data
from data.item_data.use_potions import use_potions_data
from data.gui_data.cond_strings import cond_descr_data
from data.shared_data.rarity_mod import rarity_values
from debug.timer import debug_timer
from game import Game
from gameobjects.block_level import BlockLevel
from gameobjects.entity import Entity
from gameobjects.npc import NPC
from rendering.render_order import RenderOrder
from rendering.util_functions import multiply_rgb_color


def merge_dictionaries(dicts):
    # Create a super dictionary
    merged_dict = {}
    for data in dicts:
        merged_dict = dict(merged_dict, **data)

    return merged_dict


item_data = [use_potions_data, use_bombs_data, test_equipment_data, wp_creature_data]
ITEM_DATA_MERGED = merge_dictionaries(item_data)

npc_data = [spawn_data]
NPC_DATA_MERGED = merge_dictionaries(npc_data)

architecture_data = [arch_static_data]
ARCHITECTURE_DATA_MERGED = merge_dictionaries(architecture_data)

container_data = [arch_containers_data]
CONTAINER_DATA_MERGED = merge_dictionaries(container_data)


def pick_from_data_dict_by_rarity(dic:Dict, dlvl:int=0):
    """
    picks a random key from the given dictionary items, using the 'rarity' and (optionally) 'type' values

    :param dict:
    :type dict: dict
    :param dlvl:
    :type dlvl: int
    :return:
    :rtype: dict
    """

    if dlvl > 0:  # Filter possible entries by dungeon levels first
        dic = {k: v for k, v in dic.items() if dlvl in range(*v.get('dlvls', (1, 99)))}

    while True:
        random = randint(0, 100)
        possible_items = {
            k: v for k, v in dic.items()
            if rarity_values[v.get('rarity', RarityType.COMMON)] + v.get('rarity_mod', 0) >= random
            and rarity_values[v.get('type', RarityType.COMMON)] >= random
        }
        candidates = list(possible_items.keys())
        logging.debug(f'Randomly choosing from possible candidates: {candidates}, random value was {random}')
        if len(candidates) > 0:
            candidate = choice(candidates)
            logging.debug(f'Decided on {candidate}')
            return candidate


# Data retrieving functions #
def get_generic_args(data:Dict, material:Material=None, condition:Condition=None, craftsmanship:Craftsmanship=None, bodytype:BodyType=None, randomize_color:bool=False):
    """
    Retrieves basic attributes from the data dictionary and if necessary modifies them as per material, condition and
    craftsmanship values.
    """
    char = data.get('char', '?')
    color = data.get('color', colors.white)
    name = data['name'].title()
    descr = data.get('descr', 'No description')
    ent_type = data.get('type', GenericType.DEFAULT)

    if randomize_color:
        darken = True if randint(0, 1) else False
        color = multiply_rgb_color(color, darken=darken)  # Slight color randomization for each entity

    if material:
        color = material['color']  # Update the entity's color

        if condition:
            # Append randomized condition description to the main description #
            if cond_descr_data.get(ent_type):
                descr_options = cond_descr_data[ent_type][material['type']][condition['type']]
                if descr_options:
                    cond_descr = choice(descr_options)
                    descr += f' {cond_descr}'
                else:
                    descr += f" (Description missing for {ent_type}/{material['type']}/{condition['type']})"

            # Tweak the color slightly to indicate quality level #
            # TODO Tweak as necessary
            if condition['type'] == Condition.POOR:
                color = multiply_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
            elif condition['type'] == Condition.GOOD:
                color = multiply_rgb_color(color, factor_range=(0.25, 0.25), darken=False)
            elif condition['type'] == Condition.LEGENDARY:
                color = multiply_rgb_color(color, factor_range=(0.6, 0.6), darken=False)

        if craftsmanship:
            # Append randomized condition description to the main description #
            if craft_descr_data.get(material['type']):
                descr_options = craft_descr_data[material['type']][craftsmanship['type']]
                if descr_options:
                    craft_descr = choice(descr_options)
                    descr += f' {craft_descr}'
                else:
                    descr += f" (Description missing for {material['type']}/{craftsmanship['type']})"

    if bodytype and bodytype['type'].name != 'NORMAL':
        # name = (f'{bodytype["type"].name} ' + name).title()
        # TODO extra description

        # Tweak the color slightly to indicate enemy type #
        # TODO Tweak as necessary
        # if bodytype['type'] == BodyType.SCRAWNY:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        # elif bodytype['type'] == BodyType.OBESE:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        # elif bodytype['type'] == BodyType.TINY:
        #     color = randomize_rgb_color(color, factor_range=(0.3, 0.3), darken=True)
        # elif bodytype['type'] == BodyType.SMALL:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        if bodytype['type'] == BodyType.LARGE:
            color = multiply_rgb_color(color, factor_range=(0.2, 0.2), darken=False)
        elif bodytype['type'] == BodyType.GARGANTUAN:
            color = multiply_rgb_color(color, factor_range=(0.6, 0.6), darken=False)

    return (char, color, name, descr, ent_type)

def get_generic_kwargs(data:Dict, default_render:RenderOrder=RenderOrder.BOTTOM, default_blocks:Dict=None):
    blocks = data.get('blocks', default_blocks)
    blocks = blocks.copy() if blocks else {}
    rendering = data.get('rendering', default_render)
    every_turn_start = data.get('every_turn_start', [])
    every_turn_end = data.get('every_turn_end', [])

    return {'blocks':blocks, 'render_order':rendering, 'every_turn_start':every_turn_start, 'every_turn_end':every_turn_end}


def get_material_data(data:Dict, forced:bool=False):
    """
    Retrieves material data as defined in the item_material_data dict.
    Forced can be set to a MaterialType Enum member to return the respective material.
    """
    if not forced:
        materials = {k: v for k, v in item_material_data.items() if v['type'] in data.get('materials', {})}
    else:
        materials = {k: v for k, v in item_material_data.items() if v['type'] in forced}
    material = {}
    if materials:
        key = pick_from_data_dict_by_rarity(materials)
        material = materials[key]
    return material


def get_condition_data(forced:bool=False):
    """
    Retrieves condition data as defined in the qual_cond_data dict.
    Forced can be set to a Condition Enum member to return the respective material.
    """
    dic = qual_cond_data if not forced else {k: v for k, v in qual_cond_data.items() if v['type'] in forced}
    key = pick_from_data_dict_by_rarity(dic)
    condition = qual_cond_data[key]
    return condition


def get_craftsmanship_data(forced:bool=False):
    """
    Retrieves craftsmanship data as defined in the qual_craft_data dict.
    Forced can be set to a Craftsmanship Enum member to return the respective material.
    """
    dic = qual_craft_data if not forced else {k: v for k, v in qual_craft_data.items() if v['type'] in forced}
    key = pick_from_data_dict_by_rarity(dic)
    craftsmanship = qual_craft_data[key]
    return craftsmanship


def get_bodytype_data(data:Dict, forced:bool=False):
    if forced:
        dic = {k: v for k, v in bodytype_data.items() if v['type'] in forced}
    elif data.get('bodytypes'):
        dic = {k: v for k, v in bodytype_data.items() if v['type'] in data.get('bodytypes', {})}
    else:
        dic = bodytype_data

    key = pick_from_data_dict_by_rarity(dic)
    bodytype = dic[key]

    return bodytype


# Generating Functions #
@debug_timer
def gen_npc_from_dict(data:Dict, x:int, y:int, game:Game):
    bodytype = get_bodytype_data(data, forced=False)

    arguments = (x, y, *get_generic_args(data, randomize_color=True, bodytype=bodytype))
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.ACTOR, default_blocks={BlockLevel.WALK:True})

    hp = randint(*data['max_hp'])
    stamina = randint(*data['max_stamina'])
    base_av = randint(*data['base_armor'])
    base_strength = randint(*data['base_strength'])
    vision = data.get('nat_vision', 8)
    ai_behavior = data.get('ai_behavior', Simple)
    skills = data.get('skills', None)

    # Modify values according to bodytype #
    hp_mod_multipl = bodytype.get('hp_mod_multipl', 1)
    str_multipl = bodytype.get('str_multipl', 1)
    av_mod_multipl = bodytype.get('av_mod_multipl', 1)
    hp = round(hp * hp_mod_multipl)

    base_av = round(base_av * av_mod_multipl)
    base_strength = round(base_strength * str_multipl)

    fighter_component = Fighter(hp, stamina, base_av, base_strength, vision)
    ai_component = BaseAI(behavior=ai_behavior())
    inventory_component = Inventory(capacity=12)  # Todo Placeholder #
    skills_component = None

    if skills is not None:
        skills_component = SkillList()
        for _data in skills:
            params = {key:val for key, val in _data.items() if key != 'skill'}
            skill = _data['skill'](**params)
            skills_component.add_skill(skill)

    npc = NPC(*arguments, **kwargs, bodytype=bodytype.get('type'), fighter=fighter_component, ai=ai_component,
              skills=skills_component, inventory=inventory_component)

    loadout = data.get('loadout')
    loadouts = data.get('loadouts')
    print(loadout)
    if loadouts is not None:
        loadout = pick_from_data_dict_by_rarity(loadouts, game.dlvl)
        gen_loadout(npc, loadouts[loadout], game)
    else:
        gen_loadout(npc, loadout, game)

    return npc


def gen_item_from_data(data:Dict, x:int, y:int, materials=False, conditions=False, craftsmanships=False, forced_attacktype=None):
    material = get_material_data(data, forced=materials)
    condition = get_condition_data(forced=conditions) if material else {}
    craftsmanship = get_craftsmanship_data(forced=craftsmanships) if material else {}

    arguments = [x, y, *get_generic_args(data, material=material, condition=condition, craftsmanship=craftsmanship)]
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.ITEM)

    on_use = data.get('on_use')
    equip_to = data.get('e_to')

    useable_component = None
    if on_use is not None:
        #targeted = data.get('targeted', False)
        on_use_msg = data.get('on_use_msg', '')
        charges = data.get('charges', 1)
        params = data['on_use_params']
        useable_component = Useable(on_use_effect = on_use, on_use_msg=on_use_msg, charges=charges, on_use_params=params)

    equipment_component = None
    if equip_to is not None:
        dmg_potential = data.get('dmg_potential')
        if dmg_potential:
            mat_mod = material.get('dmg_mod', 0)
            craft_mod = craftsmanship.get('dmg_mod', 0)
            cond_mod = condition.get('mod_multipl', 1)
            dmg_potential = (round(max((dmg_potential[0] + mat_mod + craft_mod) * cond_mod, 1)),
                             round(max((dmg_potential[1] + mat_mod + craft_mod) * cond_mod, 1)))

        av = data.get('av')
        if av:
            mat_mod = material.get('av_mod', 0)
            craft_mod = craftsmanship.get('av_mod', 0)
            cond_mod = condition.get('mod_multipl', 1)
            av += round((max(mat_mod + craft_mod, 1)) * cond_mod)

        block_def = data.get('block_def')
        if block_def:
            mat_mod = material.get('av_mod', 0)
            craft_mod = craftsmanship.get('av_mod', 0)
            cond_mod = condition.get('mod_multipl', 1)
            block_def += round((max(mat_mod + craft_mod, 1)) * cond_mod)

        attack_range = data.get('attack_range')
        qu_slots = data.get('qu_slots')
        l_radius = data.get('l_radius')
        two_handed = data.get('two_handed')
        attack_type = forced_attacktype if forced_attacktype else data.get('attack')
        moveset = data.get('moveset')

        if moveset:
            moveset_component = Moveset(moveset.copy())
        else:
            moveset_component = None

        equipment_component = Equipment(equip_to, dmg_potential=dmg_potential, av=av, block_def=block_def, attack_range=attack_range,
                                        qu_slots=qu_slots, l_radius=l_radius, moveset=moveset_component,
                                        two_handed=two_handed, attack_type=attack_type)

    item_component = Item(condition=condition.get('type'), craftsmanship=craftsmanship.get('type'),
                          useable=useable_component, equipment=equipment_component)

    # create the item using item_class and the arguments tuple
    i = Entity(*arguments, **kwargs, material=material.get('type'), item=item_component)

    return i


def gen_architecture(data:Dict, x:int, y:int):
    material = get_material_data(data)  # atm material only affects architecture's name and color
    arguments = [x, y, *get_generic_args(data, material=material)]
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.BOTTOM)

    container_room = data.get('container_room', None)
    on_collision = data.get('on_collision')
    on_interaction = data.get('on_interaction')

    if container_room is not None:
        inventory_component = Inventory(capacity=randint(*container_room))
    else:
        inventory_component = None
    architecture_component = Architecture(on_collision=on_collision, on_interaction=on_interaction)

    # create the static object using the arguments tuple
    arch = Entity(*arguments, **kwargs, material=material.get('type'), inventory=inventory_component,
                  architecture=architecture_component)

    return arch


def gen_loadout(actor:Entity, loadout:Dict, game:Game):
    """ creates inventory and equipment for the given actor """
    logging.debug(f'Generating loadout from {loadout} for {actor.name}({actor}).')
    equipment = loadout.get('equipment', {})
    backpack = loadout.get('backpack', {})

    for k in equipment.keys():
        item = gen_item_from_data(ITEM_DATA_MERGED.get(k), 0, 0, **equipment[k])
        actor.paperdoll.equip(item, game)

    for i in backpack:
        item = gen_item_from_data(ITEM_DATA_MERGED.get(i), 0, 0)
        actor.inventory.add(item)
