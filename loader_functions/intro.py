from config_files import colors
from rendering.render_animations import animate_explosion, animate_sparkle, animate_ray, animate_multi_ray
from rendering.render_order import RenderOrder


def play_intro(game):
    # Proof of Concept intro #
    player = game.player

    player.render_order = RenderOrder.BOTTOM
    #for i in range(5):
    # dirs = ((0,1),(0,-1),(1,0),(-1,0))
    # animate_multi_ray(*game.player.pos, game, dirs=dirs, length=5, color=colors.turquoise)
    for _i in range(3):
        animate_explosion(*game.player.pos, game, color=colors.turquoise, ignore_walls=True)
    player.render_order = RenderOrder.PLAYER