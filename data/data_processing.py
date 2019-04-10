import logging
from random import choice, randint
from typing import Dict

from components.AI.baseAI import BaseAI
from components.actors.fighter import Fighter
from components.skills.skillList import SkillList
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.items.equipment import Equipment
from components.items.item import Item
from components.items.moveset import Moveset
from components.items.useable import Useable
from config_files import colors
from data.actor_data.npc_standard import spawn_data_insects
from data.actor_data.npc_unique import spawn_data_unique
from data.architecture_data.arch_containers import arch_containers_data
from data.architecture_data.arch_static import arch_static_data
from data.data_keys import Key
from data.data_util import pick_from_data_dict_by_rarity, enum_pairs_to_kwargs, merge_dictionaries
from data.gui_data.craft_strings import craft_descr_data
from data.actor_data.act_bodytypes import bodytype_data
from data.item_data.equ_armor import equ_armor_data
from data.item_data.equ_creatures import equ_creature_data
from data.item_data.equ_offhand import equ_offhand_data
from data.item_data.equ_weapons import equ_weapon_data
from data.item_data.use_bombs import use_bombs_data
from data.item_data.use_potions import use_potions_data, use_potions_variants_data
from data.shared_data.quality_mod import qual_cond_data, qual_craft_data
from data.data_types import GenericType, Condition, BodyType, Material, Craftsmanship, Behavior
from data.shared_data.material_mod import item_material_data
from data.gui_data.cond_strings import cond_descr_data
from debug.timer import debug_timer
from game import Game
from gameobjects.block_level import BlockLevel
from gameobjects.entity import Entity
from gameobjects.special_entities import NPC
from rendering.render_order import RenderOrder
from rendering.util_functions import multiply_rgb_color


# Generate merged data dictionaries #
item_data = [use_potions_data, use_potions_variants_data, use_bombs_data, equ_creature_data, equ_weapon_data, equ_armor_data, equ_offhand_data]
npc_data = [spawn_data_insects, spawn_data_unique]
architecture_data = [arch_static_data]
container_data = [arch_containers_data]

NPC_DATA_MERGED = merge_dictionaries(npc_data)
ITEM_DATA_MERGED = merge_dictionaries(item_data)
ARCHITECTURE_DATA_MERGED = merge_dictionaries(architecture_data)
CONTAINER_DATA_MERGED = merge_dictionaries(container_data)


# Data retrieving functions #
def get_generic_args(data:Dict, material:Material=None, condition:Condition=None, craftsmanship:Craftsmanship=None, bodytype:BodyType=None, randomize_color:bool=False):
    """
    Retrieves basic attributes from the data dictionary and if necessary modifies them as per material, condition and
    craftsmanship values.
    """
    char = data.get(Key.CHAR, '?')
    color = data.get(Key.COLOR, colors.white)
    name = data[Key.NAME].title()
    descr = data.get(Key.DESCR, 'No description')
    ent_type = data.get(Key.TYPE, GenericType.DEFAULT)

    if randomize_color:
        darken = True if randint(0, 1) else False
        color = multiply_rgb_color(color, darken=darken)  # Slight color randomization for each entity

    if material:
        color = material[Key.COLOR]  # Update the entity's color

        if condition:
            # Append randomized condition description to the main description #
            if cond_descr_data.get(ent_type):
                descr_options = cond_descr_data[ent_type][material[Key.TYPE]][condition[Key.TYPE]]
                if descr_options:
                    cond_descr = choice(descr_options)
                    descr += f' {cond_descr}'
                else:
                    descr += f" (Description missing for {ent_type}/{material[Key.TYPE]}/{condition[Key.TYPE]})"

            # Tweak the color slightly to indicate quality level #
            # TODO Tweak as necessary
            if condition[Key.TYPE] == Condition.POOR:
                color = multiply_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
            elif condition[Key.TYPE] == Condition.GOOD:
                color = multiply_rgb_color(color, factor_range=(0.25, 0.25), darken=False)
            elif condition[Key.TYPE] == Condition.LEGENDARY:
                color = multiply_rgb_color(color, factor_range=(0.6, 0.6), darken=False)

        if craftsmanship:
            # Append randomized condition description to the main description #
            if craft_descr_data.get(material[Key.TYPE]):
                descr_options = craft_descr_data[material[Key.TYPE]][craftsmanship[Key.TYPE]]
                if descr_options:
                    craft_descr = choice(descr_options)
                    descr += f' {craft_descr}'
                else:
                    descr += f" (Description missing for {material[Key.TYPE]}/{craftsmanship[Key.TYPE]})"

    if bodytype and bodytype[Key.TYPE].name != 'NORMAL':
        # Tweak the color slightly to indicate enemy type #
        # TODO Tweak as necessary
        # if bodytype[Key.TYPE] == BodyType.SCRAWNY:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        # elif bodytype[Key.TYPE] == BodyType.OBESE:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        # elif bodytype[Key.TYPE] == BodyType.TINY:
        #     color = randomize_rgb_color(color, factor_range=(0.3, 0.3), darken=True)
        # elif bodytype[Key.TYPE] == BodyType.SMALL:
        #     color = randomize_rgb_color(color, factor_range=(0.2, 0.2), darken=True)
        if bodytype[Key.TYPE] == BodyType.LARGE:
            color = multiply_rgb_color(color, factor_range=(0.2, 0.2), darken=False)
        elif bodytype[Key.TYPE] == BodyType.GARGANTUAN:
            color = multiply_rgb_color(color, factor_range=(0.6, 0.6), darken=False)

    return (char, color, name, descr, ent_type)

def get_generic_kwargs(data:Dict, default_render:RenderOrder=RenderOrder.BOTTOM, default_blocks:Dict=None):
    blocks = data.get(Key.BLOCKS, default_blocks)
    blocks = blocks.copy() if blocks else {}
    rendering = data.get(Key.RENDERING, default_render)
    every_turn_start = data.get(Key.EVERY_TURN_START, [])
    every_turn_end = data.get(Key.EVERY_TURN_END, [])

    return {'blocks':blocks, 'render_order':rendering, 'every_turn_start':every_turn_start, 'every_turn_end':every_turn_end}


def get_material_data(data:Dict, forced:bool=False):
    """
    Retrieves material data as defined in the item_material_data dict.
    Forced can be set to a MaterialType Enum member to return the respective material.
    """
    if not forced:
        materials = {k: v for k, v in item_material_data.items() if v[Key.TYPE] in data.get(Key.MATERIAL, {})}
    else:
        materials = {k: v for k, v in item_material_data.items() if v[Key.TYPE] in forced}
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
    dic = qual_cond_data if not forced else {k: v for k, v in qual_cond_data.items() if v[Key.TYPE] in forced}
    key = pick_from_data_dict_by_rarity(dic)
    condition = qual_cond_data[key]
    return condition


def get_craftsmanship_data(forced:bool=False):
    """
    Retrieves craftsmanship data as defined in the qual_craft_data dict.
    Forced can be set to a Craftsmanship Enum member to return the respective material.
    """
    dic = qual_craft_data if not forced else {k: v for k, v in qual_craft_data.items() if v[Key.TYPE] in forced}
    key = pick_from_data_dict_by_rarity(dic)
    craftsmanship = qual_craft_data[key]
    return craftsmanship


def get_bodytype_data(data:Dict, forced:bool=False):
    if forced:
        dic = {k: v for k, v in bodytype_data.items() if v[Key.TYPE] in forced}
    elif data.get(Key.BODYTYPES):
        dic = {k: v for k, v in bodytype_data.items() if v[Key.TYPE] in data.get(Key.BODYTYPES, {})}
    else:
        dic = bodytype_data

    key = pick_from_data_dict_by_rarity(dic)
    bodytype = dic[key]

    return bodytype


# Generating Functions #
@debug_timer
def gen_npc_from_data(data:Dict, x:int, y:int, game:Game):
    bodytype = get_bodytype_data(data, forced=False)

    arguments = (x, y, *get_generic_args(data, randomize_color=True, bodytype=bodytype))
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.ACTOR, default_blocks={BlockLevel.WALK:True})

    # Collect npc-specific data
    hp = randint(*data[Key.MAX_HP])
    stamina = randint(*data[Key.MAX_STAMINA])
    base_av = randint(*data[Key.BASE_ARMOR])
    base_strength = randint(*data[Key.BASE_STRENGTH])
    vision = data.get(Key.BASE_VISION, 8)
    ai_behavior = data.get(Key.AI_BEHAVIOR, None)
    skills = data.get(Key.SKILLS, None)
    default_effects = data.get(Key.EFFECTS, dict())
    blood = data.get(Key.COLOR_BLOOD, colors.blood_red)

    # Setup Fighter component
    # Modify values according to bodytype
    hp_mod_multipl = bodytype.get(Key.HP_MULTIPL, 1)
    str_multipl = bodytype.get(Key.STR_MULTIPL, 1)
    av_mod_multipl = bodytype.get(Key.AV_MULTIPL, 1)
    hp = round(hp * hp_mod_multipl)
    base_av = round(base_av * av_mod_multipl)
    base_strength = round(base_strength * str_multipl)
    fighter_component = Fighter(hp, stamina, base_av, base_strength, vision, default_effects)
    ai_component = BaseAI(behavior=ai_behavior()) if ai_behavior is not None else None
    skills_component = None
    if skills is not None:
        skills_component = SkillList()
        for _data in skills:
            skill_kwargs = enum_pairs_to_kwargs(_data.items()) # Enum-Keys need to be 'translated' into strings
            del skill_kwargs['skill'] # the key words dont need to reference the skill class itself
            skill = _data[Key.SKILL](**skill_kwargs) # initialize the Skill, with derived kwargs as arguments
            skills_component.add_skill(skill)

    inventory_component = Inventory(capacity=12)  # Todo Placeholder (makes sure NPCs can equip weapons etc.) #
    npc = NPC(*arguments, **kwargs, bodytype=bodytype.get(Key.TYPE), color_blood=blood, fighter=fighter_component, ai=ai_component,
              skills=skills_component, inventory=inventory_component)

    loadout = data.get(Key.LOADOUT)
    loadouts = data.get(Key.LOADOUTS)
    if loadouts is not None:
        loadout = pick_from_data_dict_by_rarity(loadouts, game.dlvl)
        gen_loadout(npc, loadouts[loadout], game)
    else:
        gen_loadout(npc, loadout, game)

    return npc


def gen_item_from_data(data:Dict, x:int, y:int, material=False, condition=False, craftsmanship=False, forced_moveset=None):
    material = get_material_data(data, forced=material)
    condition = get_condition_data(forced=condition) if material else {}
    craftsmanship = get_craftsmanship_data(forced=craftsmanship) if material else {}

    arguments = [x, y, *get_generic_args(data, material=material, condition=condition, craftsmanship=craftsmanship)]
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.ITEM)

    on_use = data.get(Key.ON_USE)
    equip_to = data.get(Key.EQUIP_TO)

    useable_component = None
    if on_use is not None:
        #targeted = data.get('targeted', False)
        on_use_msg = data.get(Key.ON_USE_MSG, '')
        charges = data.get(Key.CHARGES, 1)
        params = data[Key.ON_USE_PARAMS]
        useable_component = Useable(on_use_effect = on_use, on_use_msg=on_use_msg, charges=charges, on_use_params=params)

    equipment_component = None
    if equip_to is not None:
        dmg_potential = data.get(Key.DMG_POTENTIAL)
        if dmg_potential:
            mat_mod = material.get(Key.DMG_FLAT, 0)
            craft_mod = craftsmanship.get(Key.DMG_FLAT, 0)
            cond_mod = condition.get(Key.MOD_MULTIPL, 1)
            dmg_potential = (round(max((dmg_potential[0] + mat_mod + craft_mod) * cond_mod, 1)),
                             round(max((dmg_potential[1] + mat_mod + craft_mod) * cond_mod, 1)))

        av = data.get(Key.AV)
        if av:
            mat_mod = material.get(Key.AV_FLAT, 0)
            craft_mod = craftsmanship.get(Key.AV_FLAT, 0)
            cond_mod = condition.get(Key.MOD_MULTIPL, 1)
            av += round((max(mat_mod + craft_mod, 1)) * cond_mod)

        block_def = data.get(Key.BLOCK_DEF)
        if block_def:
            mat_mod = material.get(Key.AV_FLAT, 0)
            craft_mod = craftsmanship.get(Key.AV_FLAT, 0)
            cond_mod = condition.get(Key.MOD_MULTIPL, 1)
            block_def += round((max(mat_mod + craft_mod, 1)) * cond_mod)

        attack_range = data.get(Key.ATTACK_RANGE)
        qu_slots = data.get(Key.QU_SLOTS)
        l_radius = data.get(Key.L_RADIUS)
        two_handed = data.get(Key.TWO_HANDED)
        #attack_type = forced_attacktype if forced_attacktype else data.get(Key.ATTACKTYPE, AttackType.NORMAL)
        if forced_moveset is None:
            moveset = data.get(Key.MOVESET)
        else:
            moveset = forced_moveset

        if moveset:
            moveset_component = Moveset(moveset.copy())
        else:
            moveset_component = None

        equipment_component = Equipment(equip_to, dmg_potential=dmg_potential, av=av, block_def=block_def, attack_range=attack_range,
                                        qu_slots=qu_slots, l_radius=l_radius, moveset=moveset_component,
                                        two_handed=two_handed)

    item_component = Item(condition=condition.get(Key.TYPE), craftsmanship=craftsmanship.get(Key.TYPE),
                          useable=useable_component, equipment=equipment_component)

    # create the item using item_class and the arguments tuple
    i = Entity(*arguments, **kwargs, material=material.get(Key.TYPE), item=item_component)

    return i


def gen_architecture(data:Dict, x:int, y:int):
    material = get_material_data(data)  # atm material only affects architecture's name and color
    arguments = [x, y, *get_generic_args(data, material=material)]
    kwargs = get_generic_kwargs(data, default_render=RenderOrder.BOTTOM)

    container_room = data.get(Key.CONTAINER_ROOM, None)
    on_collision = data.get(Key.ON_COLLISION)
    on_interaction = data.get(Key.ON_INTERACTION)

    if container_room is not None:
        inventory_component = Inventory(capacity=randint(*container_room))
    else:
        inventory_component = None
    architecture_component = Architecture(on_collision=on_collision, on_interaction=on_interaction)

    # create the static object using the arguments tuple
    arch = Entity(*arguments, **kwargs, material=material.get(Key.TYPE), inventory=inventory_component,
                  architecture=architecture_component)

    return arch


def gen_loadout(actor:Entity, loadout:Dict, game:Game):
    """ creates inventory and equipment for the given actor """
    logging.debug(f'Generating loadout from {loadout} for {actor.name}({actor}).')
    equipment = loadout.get(Key.EQUIPMENT, {})
    backpack = loadout.get(Key.BACKPACK, {})

    for key in equipment.keys():
        kwargs = enum_pairs_to_kwargs(equipment[key].items())
        item = gen_item_from_data(ITEM_DATA_MERGED.get(key), 0, 0, **kwargs)
        actor.paperdoll.equip(item, game)

    for i in backpack:
        item = gen_item_from_data(ITEM_DATA_MERGED.get(i), 0, 0)
        actor.inventory.add(item)