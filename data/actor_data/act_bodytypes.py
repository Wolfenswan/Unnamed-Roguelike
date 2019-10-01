# class BodyType(Enum):
#     NORMAL = auto()
#     SCRAWNY = auto()
#     OBESE = auto()
#     TINY = auto()
#     SMALL = auto()
#     LARGE = auto()
#     GARGANTUAN = auto()
#
from data.data_enums import Key, Mod, BodyType

bodytype_data = {
    'normal': {
        Key.TYPE: BodyType.NORMAL
    },
    'weak_1': {
        Key.TYPE: BodyType.SCRAWNY,
        Mod.STR_MULTIPL: 0.6,
        Mod.AV_MULTIPL: 0.8
    },
    'weak_2': {
        Key.TYPE: BodyType.TINY,
        Mod.HP_MULTIPL: 0.5,
        Mod.STR_MULTIPL: 0.5
    },
    'weak_3': {
        Key.TYPE: BodyType.SMALL,
        Mod.HP_MULTIPL: 0.9,
        Mod.STR_MULTIPL: 0.9
    },
    'strong_1': {
        Key.TYPE: BodyType.LARGE,
        Mod.HP_MULTIPL: 1.2,
        Mod.STR_MULTIPL: 1.2
    },
    'strong_2': {
        Key.TYPE: BodyType.OBESE,
        Mod.HP_MULTIPL: 1.75
    },
    'super_1': {
        Key.TYPE: BodyType.GARGANTUAN,
        Mod.STR_MULTIPL: 2,
        Mod.HP_MULTIPL: 2.5
    }
}