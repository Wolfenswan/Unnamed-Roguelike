from random import randint, choice


def pick_from_data_dict_by_chance(dict):
    """ picks a random item from the given dictionary, using the items 'chance' value """
    keys = list(dict.keys())
    candidate = choice(keys)

    # keep picking items at random until the rarity chance passes
    while randint(0, 100) > dict[candidate].get('chance'):
        candidate = choice(keys)

    return candidate