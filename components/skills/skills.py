import logging
from random import randint

from components.AI.behavior.simple import Simple
from components.combat.fighter_util import State
from components.skills.baseSkill import BaseSkill
from config_files import colors
from game import Game
from components.effects import Effect
from gameobjects.entity import Entity
from gameobjects.util_functions import entity_at_pos
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_to

# TODO make retrieval of often used arguments DRY

class SkillCharge(BaseSkill):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        delay = kwargs['delay']
        results = []

        d_x, d_y = user.direction_to_ent(target)
        tx, ty = target.x + d_x, target.y + d_y # The charge leads to the target pos, plus one further step in the respective direction

        user.color_bg = colors.dark_red
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(tx, ty, game), fixed=True)
        results.append({'message':Message(f'The {user.name} prepares to charge.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    def execute(self, tx: int, ty: int, game: Game, **kwargs):
        # TODO attack_string should be defined in their own data file
        user = self.owner
        user.color_bg = None  # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message': Message(f'The {user.name} charges forward!', category=MessageCategory.OBSERVATION,
                                           type=MessageType.COMBAT)})
        missed = animate_move_to(user, tx, ty, game)

        if missed is False: # if a wall is hit during the charge, damage the charging entity
            results.extend(user.f.attack_setup(user, game, dmg_mod_multipl=0.5, verb='hurts', ignore_moveset=True))
        elif not isinstance(missed, bool): # if missed is not bool, another entity was hit
            ent = missed
            if ent.fighter is not None: # if another actor was hit, that actor is damaged
                results.extend(user.f.attack_setup(ent, game, dmg_mod_multipl=2, verb='gores', ignore_moveset=True))
            elif ent.architecture is not None: # if architecture was hit, user damages itself
                results.extend(
                    user.f.attack_setup(user, game, dmg_mod_multipl=0.5, verb='rams', ignore_moveset=True))
        return results


class SkillSlam(BaseSkill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        delay = kwargs['delay']
        results = []

        user.color_bg = colors.dark_red
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(*target.pos, game), fixed=True)

        user.f.active_weapon = user.f.weapon_melee
        results.append({'message': Message(
            f'The {user.name} raises its {user.f.active_weapon.name} high above its head.', category=MessageCategory.OBSERVATION,
            type=MessageType.ALERT)})
        return results

    def execute(self, tx: int, ty: int, game: Game, **kwargs):
        user = self.owner
        user.color_bg = None  # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message': Message(f'The {user.name} slams down!', category=MessageCategory.OBSERVATION,
                                           type=MessageType.COMBAT)})
        hit = entity_at_pos(game.fighter_ents,tx, ty)
        if hit:
            if hit.fighter:
                results.extend(user.f.attack_setup(hit, game, dmg_mod_multipl=2, verb='slams', ignore_moveset=True))
        return results


class SkillExplodeSelf(BaseSkill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        results = []
        delay = kwargs.get('delay', None)
        if delay is None:
            delay = randint(kwargs['delay_min'], kwargs['delay_max'])

        user.color_bg = colors.dark_red # TODO change main color instead & make it brighter
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(game), fixed=True, exclusive=True)
        results.append({'message': Message(
            f'The {user.name} is suddenly starting to glow.',
            category=MessageCategory.OBSERVATION,
            type=MessageType.ALERT)})
        return results

    def execute(self, game:Game, **kwargs):
        results = []
        self.owner.color_bg = None  # Reset the entities bg-color, which the skill preparation had changed

        results.extend(Effect.explosion(game=game, target_pos=self.owner.pos, **self.on_activate_kwargs))
        if self.owner.f.hp > 0:
            self.owner.f.death(game)

        return results


class SkillEntangle(BaseSkill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        delay = kwargs['delay']
        results = []

        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(game), fixed=True, exclusive=True)

        return results

    def execute(self, target:Entity, game:Game, **kwargs):
        results = []
        user = self.owner
        duration = kwargs.get('duration',0)
        target.f.set_effect(State.ENTANGLED, True, duration)
        results.append({'message': Message(f'The {user.name} wraps itself around {target.name}!', category=MessageCategory.OBSERVATION,
                                           type=MessageType.COMBAT)})
        return results


class SkillHatch(BaseSkill):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def prepare(self, target:Entity, game:Game, **kwargs):
        results = []
        user = self.owner
        delay = kwargs.get('delay',None)
        if delay is None:
            delay = randint(kwargs['delay_min'], kwargs['delay_max'])
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(game), fixed=True, exclusive=True)
        return results

    def execute(self, game:Game, **kwargs):
        user = self.owner
        #results.extend(self.owner.f.death(game))
        game.map.gib_area(user.x, user.y, randint(2,4), user.color_blood, chunks=True)
        # TODO switch entity stats!
        msg1 = Message(f'{user.address_color.title()} hatches!', type=type,
                       category=MessageCategory.OBSERVATION)
        self.create_hatchling()
        results = [{'message': msg1}]
        return results

    def create_hatchling(self):
        user = self.owner
        user.char = 'h'
        user.name = 'Hatchling'
        user.color = colors.beige
        user.f.max_hp = randint(10, 15)
        user.f.hp = user.f.max_hp
        user.f.base_av = 0
        user.f.effects[State.IMMOBILE] = False
        user.ai.set_behavior(Simple())
        user.skills = None