import logging
from random import choice, randint, uniform

from components.AI.baseAI import BaseAI
from components.AI.behavior.simple import Simple
from components.actors.fighter import Fighter
from components.architecture import Architecture
from components.inventory.inventory import Inventory
from components.items.equipment import Equipment
from components.items.item import Item
from components.items.moveset import Moveset
from components.items.useable import Useable
from components.skill import Skill
from data.actor_data.skills_data import skills_data
from data.actor_data.spawn_data import spawn_data
from data.architecture_data.arch_static import arch_static_data
from data.architecture_data.arch_containers import arch_containers_data
from data.entitytypes import GenericType
from data.item_data.test_equipment import test_equipment_data
from data.item_data.use_potions import use_potions_data
from data.item_data.use_scrolls import use_scrolls_data
from gameobjects.entity import Entity
from gameobjects.npc import NPC
from rendering.render_order import RenderOrder


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


def get_generic_data(data, randomize_color = False):
    name = data['name']
    char = data['char']
    color = data['color']
    descr = data['descr']
    type = data.get('type', GenericType.DEFAULT)

    if randomize_color:
        color = tuple(int(uniform(0.5, 1) * x) for x in color) # Slight color randomization for each entity

    return (char, color, name, descr, type)


def gen_ent_from_dict(data, x, y, game):
    arguments = (x, y, *get_generic_data(data, randomize_color=True))

    hp = randint(*data['max_hp'])
    stamina = randint(*data['max_stamina'])
    defense = randint(*data['nat_armor'])
    power = randint(*data['nat_power'])
    loadouts = data.get('loadouts', None)
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

    # create the static object using the arguments tuple
    ent = NPC(*arguments, fighter=fighter_component, ai=ai_component, skills=skills_component, inventory=inventory_component)

    if loadouts is not None:
        loadout = pick_from_data_dict_by_rarity(loadouts, game.dlvl)
        gen_loadout(ent, loadouts[loadout], game)

    return ent


def gen_item_from_data(data, x, y):
    arguments = (x, y, *get_generic_data(data))

    on_use = data.get('on_use', None)
    equip_to = data.get('e_to', None)

    useable_component = None
    if on_use is not None:
    # depending on the item's class new values are received and the arguments tuple expanded
        targeting = data['targeting']
        on_use_msg = data['on_use_msg']
        on_use_params = data['on_use_params']
        useable_component = Useable(use_function = on_use, targeting = targeting, on_use_msg = on_use_msg, **on_use_params)

    equipment_component = None
    if equip_to is not None:
        dmg = data.get('dmg_range')
        av = data.get('av')
        qu_slots = data.get('qu_slots')
        l_radius = data.get('l_radius')
        two_handed = data.get('two_handed')
        moveset = data.get('moveset')

        equipment_component = Equipment(equip_to,dmg_range = dmg, av = av, qu_slots = qu_slots, l_radius = l_radius, moveset = moveset, two_handed = two_handed)

    item_component = Item(useable=useable_component, equipment=equipment_component)

    # create the item using item_class and the arguments tuple
    i = Entity(*arguments, render_order=RenderOrder.ITEM, item = item_component)

    return i


def gen_architecture(data, x, y):
    arguments = (x, y, *get_generic_data(data))

    blocks = data.get('blocks', False)
    blocks_sight = data.get('blocks_sight', False)
    container_room = data.get('container_room', (0,0))
    on_collision = data.get('on_collision')
    on_interaction = data.get('on_interaction')

    inventory_component = Inventory(randint(*container_room))
    architecture_component = Architecture(on_collision = on_collision, on_interaction = on_interaction)

    # create the static object using the arguments tuple
    arch = Entity(*arguments, blocks=blocks, blocks_sight=blocks_sight, inventory=inventory_component, architecture=architecture_component, render_order=RenderOrder.BOTTOM)

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


def pick_from_data_dict_by_rarity(dict, dlvl):
    """
    picks a random key from the given dictionary items, using the 'chance' value

    :param dict_items:
    :type dict_items: dict
    :param dlvl:
    :type dlvl: int
    :return:
    :rtype: dict
    """

    # Using the passed dict_items set a new dictionary is created, filtered by the dungeon level value
    dict = {k: v for k, v in dict.items() if dlvl in range(*v.get('dlvls', (1, 99)))}

    keys = list(dict.keys())
    type_rarity = -1

    # keep picking items at random until the rarity chances pass
    while True:
        random = randint(0, 100)
        candidate = choice(keys)
        rarity = dict[candidate]['rarity'].value + dict[candidate].get('rarity_mod', 0)

        if dict[candidate].get('type'):
            type_rarity = dict[candidate]['type'].value #dict[candidate]['rarity_type'].value

        # Check against type rarity first, then individual rarity of the item
        # TODO use random values for each check if useful
        logging.debug(f'Rarity for {candidate} is {rarity} and type rarity is {type_rarity}, random value is {random}.')
        if (type_rarity == -1 or type_rarity > random) and rarity > random:
            break

    return dict[candidate]