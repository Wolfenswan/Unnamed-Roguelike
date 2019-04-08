# class BodyType(Enum):
#     NORMAL = auto()
#     SCRAWNY = auto()
#     OBESE = auto()
#     TINY = auto()
#     SMALL = auto()
#     LARGE = auto()
#     GARGANTUAN = auto()
#
from data.data_keys import Key
from data.data_types import BodyType

bodytype_data = {
    'normal': {
        Key.TYPE: BodyType.NORMAL
    },
    'weak_1': {
        Key.TYPE: BodyType.SCRAWNY,
        Key.STR_MULTIPL: 0.6,
        Key.AV_MULTIPL: 0.8
    },
    'weak_2': {
        Key.TYPE: BodyType.TINY,
        Key.HP_MULTIPL: 0.5,
        Key.STR_MULTIPL: 0.5
    },
    'weak_3': {
        Key.TYPE: BodyType.SMALL,
        Key.HP_MULTIPL: 0.9,
        Key.STR_MULTIPL: 0.9
    },
    'strong_1': {
        Key.TYPE: BodyType.LARGE,
        Key.HP_MULTIPL: 1.2,
        Key.STR_MULTIPL: 1.2
    },
    'strong_2': {
        Key.TYPE: BodyType.OBESE,
        Key.HP_MULTIPL: 1.75
    },
    'super_1': {
        Key.TYPE: BodyType.GARGANTUAN,
        Key.STR_MULTIPL: 2,
        Key.HP_MULTIPL: 2.5
    }
}