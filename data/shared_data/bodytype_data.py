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
    'normal_bt': {
        'type': BodyType.NORMAL
    },
    'scrawny': {
        'type': BodyType.SCRAWNY
    },
    'obese': {
        'type': BodyType.OBESE
    },
    'tiny': {
        'type': BodyType.TINY
    },
    'small': {
        'type': BodyType.SMALL
    },
    'large': {
        'type': BodyType.LARGE
    },
    'gargantuan': {
        'type': BodyType.GARGANTUAN
    },
}