from components.AI.behavior.simple_melee import Simple
from components.combat.fighter_util import State
from config_files import colors
from data.actor_data.act_skills import skill_hatch
from data.data_enums import Key

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
        Key.BASE_ARMOR: 8,
        Key.BASE_STRENGTH: 0,
        Key.EFFECTS: {
            State.IMMOBILE: True
        },
        Key.SKILLS: (skill_hatch,),
    },
}