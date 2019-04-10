import logging
from random import randint, choice
from typing import Dict

from data.data_keys import Key
from data.data_types import RarityType
from data.shared_data.rarity_mod import rarity_values


def pick_from_data_dict_by_rarity(dic:Dict, dlvl:int=0):
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
        dic = {k: v for k, v in dic.items() if dlvl in range(*v.get(Key.DLVLS, (1, 99)))}

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


