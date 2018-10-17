from typing import Dict

from dataclasses import dataclass, field

from game import GameState
from gui.messages import Message, MessageCategory


@dataclass
class Useable:
    on_use_effect : Dict = field(default_factory = dict)
    on_use_msg : str = ''
    on_use_params : Dict = field(default_factory = dict)
    charges : int = 1

    def __post_init__(self):
        self.on_use_function = self.on_use_effect.get('on_execution')
        self.targeted = self.on_use_effect.get('targeted', False)

    def use(self, user, game, **kwargs):

        item_entity = self.owner.owner
        results = []

        if self.on_use_function is None:
            results.append({'message': Message(f'The {item_entity.name} cannot be used like this.', category=MessageCategory.OBSERVATION)})
        else:
            if self.targeted and not game.state in [GameState.CURSOR_ACTIVE, GameState.CURSOR_TARGETING]:
                results.append({'targeting': item_entity,'message': Message('Move the cursor over the intended target, press Enter to confirm.')})
            else:
                item_use_results = self.on_use_function(game=game, user=user, used_item=item_entity, **kwargs, **self.on_use_params, **self.on_use_effect)
                if self.on_use_msg:
                    item_use_results.append({'message': Message(self.on_use_msg)})
                results.extend(item_use_results)

                self.charges -= 1
                if self.charges == 0:
                    results.append({'consumed':item_entity})

        return results