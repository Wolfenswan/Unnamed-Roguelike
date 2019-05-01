import logging
from random import randint, choice
from typing import Dict

from data.data_keys import Key
from data.data_types import RarityType
from data.shared_data.rarity_mod import rarity_values


def filter_data_dict(dic:Dict, dlvl:int=0):
    """
    Picks a random key from the given dictionary items

    The function first creates a mini-dictionary of possible candidates, using two rarity parameters:
    a) Key.RARITY: the rarity value of the object itself, assigned in the data files
    b) Key.TYPE: the rarity value of the material, assigned to the object (e.g. steel being rarer than iron)

    Then it randomly picks a key from these candidates using choice()

    :param dict:
    :type dict: dict
    :param dlvl:
    :type dlvl: int
    :return:
    :rtype: dict
    """

    if dlvl > 0:  # Filter possible entries by dungeon levels first
        dic = {
            k: v for k, v in dic.items()
            if dlvl_check(dlvl, v)
        }

    while True:
        random = randint(0, 100)
        possible_items = { # Create dictionary of candidates
            k: v for k, v in dic.items()
            if rarity_values[v.get(Key.RARITY, RarityType.COMMON)] + v.get(Key.RARITY_MOD, 0) >= random
            and rarity_values[v.get(Key.TYPE, RarityType.COMMON)] >= random
        }
        candidates = list(possible_items.keys())
        logging.debug(f'Randomly choosing from possible candidates: {candidates}, random value was {random}')
        if len(candidates) > 0:
            candidate = choice(candidates)
            logging.debug(f'Decided on {candidate}')
            return candidate


def dlvl_check(dlvl, data, factor=25):
    """
    Checks spawn chance for given data-entry in the given dungeon-level. Each level below/above their spawn range, there's
    a 25% less chance to spawn.
    Returns True or False. Data with UNIQUE rarity can only spawn within their dungeon-level-range.
    """
    dlvls = data.get(Key.DLVLS, (1, 1000))

    if dlvl in range(*dlvls):
        return True

    if data.get(Key.RARITY, RarityType.COMMON) == RarityType.UNIQUE:
        return False

    chance = -1
    if dlvl not in range(*dlvls):
        if dlvl < dlvls[0] and dlvls[0] - dlvl <= 6:
            chance = max(1,100 - (dlvls[0] - dlvl) * factor)
        elif dlvl > dlvls[1] and dlvl - dlvls[1] <= 6:
            chance = max(1,100 - (dlvl - dlvls[1]) * factor)

    return chance >= randint(0,100)


def enum_pairs_to_kwargs(dictionary:Dict):
    # Enum-keys can't be passed as key words, so a temporary dictionary using their names as keys is created
    # E.g.: Key.NAME -> 'name'
    return {_k.name.lower(): _v for _k, _v in dictionary}


def merge_dictionaries(dicts):
    # Create a super dictionary
    merged_dict = {}
    for data in dicts:
        merged_dict = dict(merged_dict, **data)

    return merged_dict


