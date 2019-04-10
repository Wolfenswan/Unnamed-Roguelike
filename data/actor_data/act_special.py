from components.actors.fighter_util import State
from config_files import colors
from data.actor_data.act_skills import skill_hatch
from data.data_keys import Key
from data.data_types import RarityType

# This dictionary is omitted from the merged NPC_SPAWNING array it's purpose is to cover special actors that are
# not spawned by default but e.g. created by other monsters
spawn_data_special = {
    'egg': {
            Key.NAME: 'Egg',
            Key.CHAR: 'e',
            Key.COLOR: colors.beige,
            Key.DESCR: 'TODO EGG.',
            Key.MAX_HP: 1,
            Key.MAX_STAMINA: 100,
            Key.BASE_ARMOR: 10,
            Key.EFFECTS: {
                State.IMMOBILE: True
            },
            Key.SKILLS: (skill_hatch,),
        }
}