from enum import Enum
from typing import Tuple

class Direction(Enum):
    NONE: Tuple[int, int] = (0, 0)
    CENTER: Tuple[int, int] = NONE

    NORTH: Tuple[int, int] = (0, -1)
    UP: Tuple[int, int] = NORTH
    TOP: Tuple[int, int] = NORTH

    WEST: Tuple[int, int] = (-1, 0)
    LEFT: Tuple[int, int] = WEST

    EAST: Tuple[int, int] = (1, 0)
    RIGHT: Tuple[int, int] = EAST

    SOUTH: Tuple[int, int] = (0, 1)
    DOWN: Tuple[int, int] = SOUTH
    BOTTOM: Tuple[int, int] = SOUTH

    NORTH_WEST: Tuple[int, int] = (-1,-1)
    UP_LEFT: Tuple[int, int] = NORTH_WEST
    TOP_LEFT: Tuple[int, int] = NORTH_WEST

    NORTH_EAST: Tuple[int, int] = (1, -1)
    UP_RIGHT: Tuple[int, int] = NORTH_EAST
    TOP_RIGHT: Tuple[int, int] = NORTH_EAST

    SOUTH_WEST: Tuple[int, int] = (-1, 1)
    DOWN_LEFT: Tuple[int, int] = SOUTH_WEST
    BOTTOM_LEFT: Tuple[int, int] = SOUTH_WEST

    SOUTH_EAST: Tuple[int, int] = (1, 1)
    DOWN_RIGHT: Tuple[int, int] = SOUTH_EAST
    BOTTOM_RIGHT: Tuple[int, int] = SOUTH_EAST


class RelativeDirection(Enum):
    LEFT: str = 'left'
    RIGHT: str = 'right'
    LEFT_BACK: str ='left-back'
    RIGHT_BACK: str ='right-back'
    BEHIND: str = 'behind'


DIRECTIONS_CIRCLE = [dir.value for dir in [Direction.NORTH, Direction.NORTH_EAST, Direction.EAST, Direction.SOUTH_EAST,
                    Direction.SOUTH, Direction.SOUTH_WEST, Direction.WEST, Direction.NORTH_WEST]]


def relative_dir(dir:Direction, rel_dir:RelativeDirection):
    i = DIRECTIONS_CIRCLE.index(dir)
    if rel_dir == RelativeDirection.BEHIND:
        dir_x, dir_y = dir
        return (dir_x*2, dir_y*2)
    if rel_dir == RelativeDirection.LEFT:
        return DIRECTIONS_CIRCLE[(i + 8 - 1)%8]
    if rel_dir == RelativeDirection.LEFT_BACK:
        return DIRECTIONS_CIRCLE[(i + 7 - 1) % 8]
    if rel_dir == RelativeDirection.RIGHT:
        return DIRECTIONS_CIRCLE[(i + 1) % 8]
    if rel_dir == RelativeDirection.RIGHT_BACK:
        return DIRECTIONS_CIRCLE[(i + 2) % 8]


def direction_between_pos(x1, y1, x2, y2):
    dx, dy = 0, 0
    x_plane = x2 - x1
    y_plane = y2 - y1

    if x_plane > 0:
        dx = 1
    elif x_plane < 0:
        dx = -1

    if y_plane > 0:
        dy = 1
    elif y_plane < 0:
        dy = -1

    return dx, dy