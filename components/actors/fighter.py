import tcod

import game
from common.game_states import GameStates
from rendering.render_functions import RenderOrder


class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': f'{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.'})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': f'{self.owner.name.capitalize()} attacks {target.name} but does no damage.'})

        return results

    def death(self):
        ent = self.owner
        
        if ent.is_player:
            ent.char = '%'
            ent.color = tcod.dark_red

            return 'You died!'
        else:
            death_message = f'The {ent.name.capitalize()} is dead!'
            
            ent.char = '%'
            ent.color = tcod.dark_red
            ent.blocks = False
            ent.render_order = RenderOrder.CORPSE
            ent.fighter = None
            ent.ai = None
            ent.name = 'remains of ' + ent.name

            return death_message