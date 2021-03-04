from config_files import colors
from data.data_enums import Key, LevelType

level_types_data = {
    LevelType.DUNGEON: {
        Key.NAME : 'Dungeon',
        Key.DLVLS: (1,2),
        Key.ROOM_FUZZY_CHANCE : 0,
        Key.DRUNK_TUNNEL_CHANCE : 0,
        Key.RANDOMIZE_TUNNEL_CONNECTIONS : False,
        Key.ROOM_MIN_SIZE : 5,
        Key.ROOM_MAX_SIZE : 16,
        Key.LEVEL_COLORS : (colors.granite,colors.stone),
    },
    LevelType.CAVE: {
        Key.NAME : 'Cave',
        Key.DLVLS: (5,6),
        Key.ROOM_FUZZY_CHANCE : 60,
        Key.DRUNK_TUNNEL_CHANCE : 80,
        Key.RANDOMIZE_TUNNEL_CONNECTIONS : True,
        Key.ROOM_MIN_SIZE : 3,
        Key.ROOM_MAX_SIZE : 30,
        Key.LEVEL_COLORS : (colors.clay,colors.granite),
    },
    LevelType.MINE:{
        Key.NAME : 'Mine',
        Key.DLVLS: (3,4),
        Key.ROOM_FUZZY_CHANCE : 25,
        Key.DRUNK_TUNNEL_CHANCE : 40,
        Key.RANDOMIZE_TUNNEL_CONNECTIONS : True,
        Key.ROOM_MIN_SIZE : 3,
        Key.ROOM_MAX_SIZE : 12,
        Key.LEVEL_COLORS : (colors.clay,colors.granite),
    }
}