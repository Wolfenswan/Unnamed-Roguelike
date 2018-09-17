# class BodyType(Enum):
#     NORMAL = auto()
#     SCRAWNY = auto()
#     OBESE = auto()
#     TINY = auto()
#     SMALL = auto()
#     LARGE = auto()
#     GARGANTUAN = auto()
#
from data.shared_data.types_data import BodyType

bodytype_data = {
    'normal': {
        'type': BodyType.NORMAL
    },
    'scrawny': {
        'type': BodyType.SCRAWNY,
        'dmg_mod_multipl': 0.6,
        'av_mod_multipl': 0.8
    },
    'obese': {
        'type': BodyType.OBESE,
        'hp_mod_multipl': 1.5
    },
    'tiny': {
        'type': BodyType.TINY,
        'hp_mod_multipl': 0.5,
        'dmg_mod_multipl': 0.5
    },
    'small': {
        'type': BodyType.SMALL,
        'hp_mod_multipl': 0.9,
        'dmg_mod_multipl': 0.9
    },
    'large': {
        'type': BodyType.LARGE,
        'hp_mod_multipl': 1.2,
        'dmg_mod_multipl': 1.2
    },
    'gargantuan': {
        'type': BodyType.GARGANTUAN,
        'dmg_mod_multipl': 2,
        'hp_mod_multipl': 2.5
    },
}