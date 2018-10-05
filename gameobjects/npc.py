import logging
import math
from random import choice

import tcod

from data.data_types import GenericType
from gameobjects.block_level import BlockLevel
from gameobjects.entity import Entity
from gui.messages import Message, MessageType, MessageCategory
from rendering.render_order import RenderOrder





class NPC(Entity):
    """ Class for the all active non-player objects """

    def __init__(self, x, y, char, color, name, descr, type=GenericType.DEFAULT, render_order=RenderOrder.ACTOR, bodytype=None, barks=None, fighter=None, ai=None, inventory=None, skills=None):
        super().__init__(x, y, char, color, name, descr, type=type, blocks={BlockLevel.WALK:True}, render_order=render_order, bodytype=bodytype, fighter=fighter, ai=ai, skills=skills, inventory=inventory)

        self.barks = barks

    def move_towards(self, target, game):
        game_map = game.map
        blocking_ents = game.walk_blocking_ents

        dx, dy = self.direction_to_ent(target)
        # dx = target_x - self.x
        # dy = target_y - self.y
        #distance = self.distance_to_ent(target)
        # dx = int(round(dx / distance))
        # dy = int(round(dy / distance))
        #print(dx, dy, distance)

        if not game_map.is_blocked(self.x + dx, self.y + dy, blocking_ents):
            self.move(dx, dy)
        # if not (game_map.is_wall(self.x + dx, self.y + dy) or
        #         entity_at_pos(entities, self.x + dx, self.y + dy)):

    def move_astar(self, target, game):
        game_map = game.map
        blocking_ents = game.walk_blocking_ents

        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[(x1,y1)].block_sight,
                                           not game_map.tiles[(x1,y1)].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in blocking_ents:
            if entity.blocks.get(BlockLevel.WALK, False) and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            logging.debug(f'{self.name} could not find a* path. falling back to regular movement')
            self.move_towards(target, game)

    def bark(self,type):
        """ make some noise """
        results = []
        if self.barks is not None:
            try:
                bark = choice(self.barks[type])
            except:
                logging.error('Could not find bark-type {0} in {1}.'.format(type, self.barks))
            else:
                results.append({'message':Message(f'The {self.name} {bark}', type=MessageType.FLUFF, category=MessageCategory.OBSERVATION)})
        return results
