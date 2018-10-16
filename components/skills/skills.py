from components.skills.baseSkill import BaseSkill
from components.skills.skillConditions import SkillCondition
from config_files import colors
from game import Game
from gameobjects.entity import Entity
from gameobjects.util_functions import entity_at_pos
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_animations import animate_move_to


class SkillCharge(BaseSkill):

    def __init__(self, **kwargs):
        self.params = kwargs
        if kwargs.get('name') is None:
            self.params['name'] = 'Charge'
        if kwargs.get('activate_conditions') is None:
            self.params['activate_conditions'] = {SkillCondition.distance_to}

        super().__init__(**self.params)

    def activate(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        delay = kwargs['delay']
        results = []

        d_x, d_y = user.direction_to_ent(target)
        tx, ty = target.x + d_x, target.y + d_y

        user.color_bg = colors.dark_red
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(tx, ty, game), fixed=True)
        results.append({'message':Message(f'The {user.name} prepares to charge.', category=MessageCategory.OBSERVATION, type=MessageType.ALERT)})
        return results

    def execute(self, tx: int, ty: int, game: Game):
        # TODO attack_string should be defined in their own data file
        user = self.owner
        user.color_bg = None  # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message': Message(f'The {user.name} charges forward!', category=MessageCategory.OBSERVATION,
                                           type=MessageType.COMBAT)})
        hit = animate_move_to(user, tx, ty, game)
        if hit:
            if hit.fighter:
                results.extend(user.fighter.attack_setup(hit, game, dmg_mod_multipl=2, verb='gores', ignore_moveset=True))
            elif hit.architecture:
                results.extend(
                    user.fighter.attack_setup(user, game, dmg_mod_multipl=0.5, verb='rams', ignore_moveset=True))
        elif hit is False:  # If a wall is hit during the charge, damage the charging entity
            results.extend(user.fighter.attack_setup(user, game, dmg_mod_multipl=0.5, verb='rams', ignore_moveset=True))
        return results


class SkillSlam(BaseSkill):
    def __init__(self, **kwargs):
        self.params = kwargs
        if kwargs.get('name') is None:
            self.params['name'] = 'Slam'
        if kwargs.get('activate_conditions') is None:
            self.params['activate_conditions'] = {SkillCondition.distance_to}

        super().__init__(**self.params)

    def activate(self, target:Entity, game:Game, **kwargs):
        user = self.owner
        delay = kwargs['delay']
        results = []

        user.color_bg = colors.dark_red
        user.actionplan.add_to_queue(execute_in=delay, planned_function=self.execute,
                                     planned_function_args=(*target.pos, game), fixed=True)
        results.append({'message': Message(
            f'The {user.name} raises its {user.fighter.active_weapon.name} high above its head.', category=MessageCategory.OBSERVATION,
            type=MessageType.ALERT)})
        return results

    def execute(self, tx: int, ty: int, game: Game):
        user = self.owner
        user.color_bg = None  # Reset the entities bg-color, which the skill preparation had changed

        results = []
        results.append({'message': Message(f'The {user.name} slams down!', category=MessageCategory.OBSERVATION,
                                           type=MessageType.COMBAT)})
        hit = entity_at_pos(game.fighter_ents,tx, ty)
        if hit:
            if hit.fighter:
                results.extend(user.fighter.attack_setup(hit, game, dmg_mod_multipl=2, verb='slams', ignore_moveset=True))
        return results


class SkillExplode(BaseSkill):
    def __init__(self, **kwargs):
        self.params = kwargs
        if kwargs.get('name') is None:
            self.params['name'] = 'Explode'
        if kwargs.get('activate_conditions') is None:
            self.params['activate_conditions'] = {SkillCondition.distance_to}

        super().__init__(**self.params)

    def activate(self, *args, **kwargs):
        pass

    def execute(self):
        pass