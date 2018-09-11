import logging
from random import choice, randint

from components.AI.baseAI import BaseAI
from components.AI.behavior.simple import Simple
from components.actors.fighter import Fighter
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.items.equipment import Equipment
from components.items.item import Item
from components.items.useable import Useable
from components.skill import Skill
from config_files import colors
from data.actor_data.skills_data import skills_data
from data.actor_data.spawn_data import spawn_data
from data.architecture_data.arch_static import arch_static_data
from data.architecture_data.arch_containers import arch_containers_data
from data.descr_data.craft_descr import craft_descr_data
from data.shared_data.quality_data import qual_cond_data, qual_craft_data
from data.shared_data.types_data import GenericType, Condition, RarityType
from data.shared_data.material_data import item_material_data
from data.item_data.test_equipment import test_equipment_data
from data.item_data.use_potions import use_potions_data
from data.item_data.use_scrolls import use_scrolls_data
from data.descr_data.cond_descr import cond_descr_data
from data.shared_data.rarity_data import rarity_values
from gameobjects.entity import Entity
from gameobjects.npc import NPC
from rendering.render_order import RenderOrder
from rendering.util_functions import randomize_rgb_color


def merge_dictionaries(dicts):
    # Create a super dictionary
    merged_dict = {}
    for data in dicts:
        merged_dict = dict(merged_dict, **data)

    return merged_dict


item_data = [use_scrolls_data, use_potions_data, test_equipment_data]
ITEM_DATA_MERGED = merge_dictionaries(item_data)

actor_data = [spawn_data]
ACTOR_DATA_MERGED = merge_dictionaries(actor_data)

architecture_data = [arch_static_data]
ARCHITECTURE_DATA_MERGED = merge_dictionaries(architecture_data)

container_data = [arch_containers_data]
CONTAINER_DATA_MERGED = merge_dictionaries(container_data)


def pick_from_data_dict_by_rarity(dict, dlvl=0):
    """
    picks a random key from the given dictionary items, using the 'chance' value

    :param dict:
    :type dict: dict
    :param dlvl:
    :type dlvl: int
    :return:
    :rtype: dict
    """

    # Using the passed dict_items set a new dictionary is created, filtered by the dungeon level value
    if dlvl > 0:
        dict = {k: v for k, v in dict.items() if dlvl in range(*v.get('dlvls', (1, 99)))}

    keys = list(dict.keys())
    type_rarity = -1

    # keep picking items at random until the rarity chances pass
    while True:
        random = randint(0, 100)
        candidate = choice(keys)
        logging.debug(f'Trying to calculate rarity for {candidate}')

        # If an overall type is assigned to the candidate, calculate its rarity weight
        if dict[candidate].get('type'):
            type = dict[candidate]['type']
            type_rarity = rarity_values.get(type, -1)

        # Set the rarity for the individual item. Defaults to 100 if the value is not set in the data entry.
        rarity_type = dict[candidate].get('rarity', RarityType.COMMON)
        item_rarity = rarity_values[rarity_type] + dict[candidate].get('rarity_mod', 0)

        # Check against type rarity first, then individual rarity of the item
        # TODO use random values for each check if useful
        logging.debug(f'Rarity for {candidate} is {item_rarity} and type rarity is {type_rarity}, random value is {random}.')
        if (type_rarity == -1 or type_rarity > random) and item_rarity > random:
            break
        logging.debug(f'Dropping {candidate}')

    return candidate


def get_generic_data(data, randomize_color = False):
    char = data['char']
    color = data.get('color', colors.white)
    name = data['name'].title()
    descr = data.get('descr', 'No description')
    type = data.get('type', GenericType.DEFAULT)

    if randomize_color:
        darken = True if randint(0, 1) else False
        color = randomize_rgb_color(color, darken = darken) # Slight color randomization for each entity
        print(color)

    return (char, color, name, descr, type)


def get_material_data(data, arguments):
    materials = {k:v for k, v in item_material_data.items() if v['type'] in data.get('materials',{})}
    if materials:
        key = pick_from_data_dict_by_rarity(materials)
        material = materials[key]
        arguments[3] = material['color'] # Update the entity's color
        arguments[4] = f"{material['name']} {arguments[4]}".title() # Update the entity's name
    else:
        material = {}

    return material


def get_condition_data(material, arguments):
    if material:
        key = pick_from_data_dict_by_rarity(qual_cond_data)
        condition = qual_cond_data[key]

        # Append randomized condition description to the main description #
        type = arguments[6]
        if cond_descr_data.get(type):
            cond_descr = choice(cond_descr_data[type][material['type']][condition['type']])
            arguments[5] += f' {cond_descr}'

        # Tweak the color slightly to indicate quality level #
        # TODO Tweak as necessary
        if condition['type'] == Condition.POOR:
            arguments[3] = randomize_rgb_color(arguments[3], factor_range=(0.2, 0.2), darken=True)
        elif condition['type'] == Condition.GOOD:
            arguments[3] = randomize_rgb_color(arguments[3], factor_range=(0.2, 0.2), darken=False)
        elif condition['type'] == Condition.LEGENDARY:
            arguments[3] = randomize_rgb_color(arguments[3], factor_range=(0.4, 0.4), darken=False)
    else:
        condition = {}

    return condition


def get_craftsmanship_data(material, arguments):
    if material:
        key = pick_from_data_dict_by_rarity(qual_craft_data)
        craftsmanship = qual_craft_data[key]

        # Append randomized condition description to the main description #
        if craft_descr_data.get(material['type']):
            craft_descr = choice(craft_descr_data[material['type']][craftsmanship['type']])
            print(craft_descr)
            arguments[5] += f' {craft_descr}'
    else:
        craftsmanship = {}

    return craftsmanship



def gen_npc_from_dict(data, x, y, game):
    arguments = (x, y, *get_generic_data(data, randomize_color=True))

    hp = randint(*data['max_hp'])
    stamina = randint(*data['max_stamina'])
    defense = randint(*data['nat_armor'])
    power = randint(*data['nat_power'])
    loadouts = data.get('loadouts')
    vision = data.get('nat_vision', 8)
    ai_movement = data.get('ai_movement', Simple)
    ai_attack = data.get('ai_attack', Simple)
    skills = data.get('skills', None)

    fighter_component = Fighter(hp, stamina, defense, power, vision)
    ai_component = BaseAI(movement=ai_movement(), attack=ai_attack())
    inventory_component = Inventory(12) # Todo Placeholder #
    skills_component = None

    if skills is not None:
        skills_component = {}
        for k in skills:
            skill = Skill(**skills_data[k])
            skills_component[k] = (skill)

    npc = NPC(*arguments, fighter=fighter_component, ai=ai_component, skills=skills_component, inventory=inventory_component)

    if loadouts is not None:
        loadout = pick_from_data_dict_by_rarity(loadouts, game.dlvl)
        gen_loadout(npc, loadouts[loadout], game)

    return npc


def gen_item_from_data(data, x, y, force_material=False, force_condition=False, force_craftsmanship=False):
    arguments = [x, y, *get_generic_data(data)]

    on_use = data.get('on_use', None)
    equip_to = data.get('e_to', None)
    if not force_material:
        material = get_material_data(data, arguments)
    if not force_condition:
        condition = get_condition_data(material, arguments)
    if not force_craftsmanship:
        craftsmanship = get_craftsmanship_data(material, arguments)

    useable_component = None
    if on_use is not None:
    # depending on the item's class new values are received and the arguments tuple expanded
        targeting = data['targeting']
        on_use_msg = data['on_use_msg']
        on_use_params = data['on_use_params']
        useable_component = Useable(use_function = on_use, targeting = targeting, on_use_msg = on_use_msg, **on_use_params)

    equipment_component = None
    if equip_to is not None:
        dmg_range = data.get('dmg_range')
        if dmg_range:
            mat_mod = material.get('dmg_mod',0)
            cond_mod = condition.get('dmg_mod', 0)
            dmg_range = (max((dmg_range[0] + mat_mod + cond_mod),1), dmg_range[1] + mat_mod + cond_mod)

        av = data.get('av')
        if av:
            mat_mod = material.get('av_mod', 0)
            cond_mod = condition.get('av_mod', 0)
            av += max(mat_mod + cond_mod,1)

        qu_slots = data.get('qu_slots')
        l_radius = data.get('l_radius')
        two_handed = data.get('two_handed')
        moveset = data.get('moveset')

        equipment_component = Equipment(equip_to, dmg_range = dmg_range, av = av, qu_slots = qu_slots, l_radius = l_radius, moveset = moveset, two_handed = two_handed)

    item_component = Item(condition=condition.get('type'), craftsmanship=craftsmanship.get('type'), useable=useable_component, equipment=equipment_component)

    # create the item using item_class and the arguments tuple
    i = Entity(*arguments, material=material.get('type'), render_order=RenderOrder.ITEM, item = item_component)

    return i


def gen_architecture(data, x, y):
    arguments = [x, y, *get_generic_data(data)]
    material = get_material_data(data, arguments) # atm material only affects architecture's name and color

    blocks = data.get('blocks', False)
    blocks_sight = data.get('blocks_sight', False)
    container_room = data.get('container_room', (0,0))
    on_collision = data.get('on_collision')
    on_interaction = data.get('on_interaction')

    inventory_component = Inventory(randint(*container_room))
    architecture_component = Architecture(on_collision = on_collision, on_interaction = on_interaction)

    # create the static object using the arguments tuple
    arch = Entity(*arguments, material=material.get('type'), blocks=blocks, blocks_sight=blocks_sight, inventory=inventory_component, architecture=architecture_component, render_order=RenderOrder.BOTTOM)

    return arch


def gen_loadout(actor, loadout, game):
    """ creates inventory and equipment for the given actor """
    logging.debug(f'Generating loadout from {loadout} for {actor.name}({actor}).')
    for e in loadout.get('equipment',[]):
        item = gen_item_from_data(ITEM_DATA_MERGED.get(e), 0, 0)
        actor.paperdoll.equip(item, game)

    for i in loadout.get('backpack',[]):
        item = gen_item_from_data(ITEM_DATA_MERGED.get(i), 0, 0)
        actor.inventory.add(item)
