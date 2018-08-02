from random import randint

import tcod

from components.AI.confusedmonster import ConfusedMonster
from gui.messages import Message, MessageType


def heal_entity(**kwargs):
    entity = kwargs.get('caster')
    amount = kwargs.get('pwr')

    if type(amount) is not int:
        amount = randint(*amount)

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', MessageType.INFO_GENERIC)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', MessageType.INFO_GOOD)})

    return results

def cast_lightning_on(**kwargs):
    caster = kwargs.get('caster')
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to_ent(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(f'A lighting bolt strikes the {target.name} with a loud thunder! The damage is {damage}')})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.')})

    return results

def cast_fireball_on(**kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('dmg')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.')})
        return results

    results.append({'consumed': True, 'message': Message(f'The fireball explodes, burning everything within {radius} tiles!')})

    for entity in entities:
        if entity.distance_to_pos(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message(f'The {entity.name} gets burned for {damage} hit points.')})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse_on(**kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.')})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message(f'The eyes of the {entity.name} look vacant, as he starts to stumble around!')})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.')})

    return results