from gameobjects.items.equipment import Armor
from common import colors

ARM_CHAR = ']'
ARM_COLOR = colors.brass
ARM_CLASS = Armor
ARM_EQUIP = 'torso'  # which extremity the item is equipped to
ARM_TYPE = 'armor'  # which slot it will take

arm_body_data = {
    'leather_brittle': {
        'name': 'Brittle Leather Armor',
        'descr': 'A squeaking old piece of leather armor.',
        'chance': 50,
        'dlvls': range(1, 99),
        "char": ARM_CHAR,
        "color": ARM_COLOR,
        'item_class': ARM_CLASS,
        'e_to': ARM_EQUIP,
        'e_type': ARM_TYPE,
        'av': 3,
        'weight': 1
    },
    'leather_vest': {
        'name': 'Leather Vest',
        'descr': 'A light leather vest with extra pcokets.',
        'chance': 50,
        'dlvls': range(1, 99),
        "char": ARM_CHAR,
        "color": ARM_COLOR,
        'item_class': ARM_CLASS,
        'e_to': ARM_EQUIP,
        'e_type': ARM_TYPE,
        'av': 2,
        'slots': 2,
        'weight': 1
    },
    'leather_orc': {
        'name': 'Orcish Leather Armor',
        'descr': 'Bloody stains and rot adorn this failed attempt at armor making.',
        'chance': -1,
        'dlvls': range(1, 99),
        "char": ARM_CHAR,
        "color": ARM_COLOR,
        'item_class': ARM_CLASS,
        'e_to': ARM_EQUIP,
        'e_type': ARM_TYPE,
        'av': 2,
        'weight': 1
    }
}