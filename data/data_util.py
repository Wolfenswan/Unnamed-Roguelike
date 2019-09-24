import logging
from random import randint, choice
from typing import Dict

from data.data_keys import Key
from data.data_types import RarityType
from data.shared_data.rarity_mod import rarity_values


def filter_data_dict(dic:Dict, dlvl:int=0):
    """
    Picks a random key from the given dictionary items

    The function first creates a sub-dictionary of possible candidates, using the possible range of dungeon levels and
    two rarity parameters:
    a) Key.RARITY: the rarity value of the object itself, assigned in the data files
    b) Key.TYPE: the rarity value of the material, assigned to the object (e.g. steel being rarer than iron)

    Then it randomly picks a key from these candidates using choice()

    :param dict: data dictionary
    :type dict: dict
    :param dlvl: the dungeon level to consider (0: ignore dungeon level)
    :type dlvl: int
    :return: key referring to a data-entry
    :rtype: str
    """
    if dlvl > 0:  # Filter possible entries by dungeon levels first
        dic = {
            k: v for k, v in dic.items() if dlvl_filter(dlvl, v)
        }

    if len(dic) > 0:
        while True:
            random = randint(0, 100)
            possible_items = {
                # Create merged dictionary of candidates, checking against both their own rarity
                # and the rarity of their types
                k: v for k, v in dic.items()
                if rarity_values[v.get(Key.RARITY, RarityType.COMMON)] + v.get(Key.RARITY_MOD, 0) >= random
                and rarity_values[v.get(Key.TYPE, RarityType.COMMON)] >= random
            }
            candidates = list(possible_items.keys())
            logging.debug(f'Filtered candidates with random chance: {random}. Result: {candidates}')
            if len(candidates) > 0:
                candidate = choice(candidates)
                logging.debug(f'Decided on {candidate}')
                return candidate

    logging.error(f'Data-dictionary had length of 0 after initial dlvl-filter.')


def dlvl_filter(dlvl, data, factor=25):
    """
    Checks spawn chance for given data-entry in the given dungeon-level.
    Each level outside their spawn range reduces the spawn chance by 25%.
    Returns True or False.
    """
    dlvls = data.get(Key.DLVLS, (0, 1000))

    if dlvl in inclusive_range(*dlvls):
        return True

    # if data.get(Key.RARITY, RarityType.COMMON) == RarityType.UNIQUE:
    #     return False

    chance = -1
    if factor >= 0 and dlvl not in inclusive_range(*dlvls):
        diff = (dlvls[0] - dlvl, dlvl - dlvls[1])
        if dlvl < dlvls[0] and diff[0] <= 5:
            chance = max(1,100 - diff[0] * factor)
        elif dlvl > dlvls[1] and diff[1] <= 5:
            chance = max(1,100 - diff[1] * factor)

    return chance > randint(0,100)


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


def inclusive_range(x, y):
    """ Returns a range from x to y including y """
    return range(x, y+1)

