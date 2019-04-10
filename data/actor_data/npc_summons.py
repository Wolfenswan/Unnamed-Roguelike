from components.AI.behavior.simple import Simple
from components.actors.fighter_util import State
from config_files import colors
from data.actor_data.act_skills import skill_hatch
from data.data_keys import Key

spawn_data_summons = {
    'hatchling_egg': {
        Key.NAME: 'Egg',
        Key.CHAR: 'e',
        Key.COLOR: colors.beige,
        Key.COLOR_BLOOD: colors.blood_slime,
        Key.DESCR: 'TODO EGG.',
        Key.AI_BEHAVIOR: Simple,
        Key.MAX_HP: 1,
        Key.MAX_STAMINA: 50,
        Key.BASE_ARMOR: 10,
        Key.BASE_STRENGTH: 5,
        Key.EFFECTS: {
            State.IMMOBILE: True
        },
        Key.SKILLS: (skill_hatch,),
    },
}