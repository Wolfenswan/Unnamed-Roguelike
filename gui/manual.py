import tcod

from config_files import cfg, colors
from gui.menus import menu_loop
from rendering.util_functions import setup_console


def display_manual():
    """displays the game's manual"""
    with open('resources/manual.txt') as manfile:
        # TODO: Use RegEx for nicer split-lines in manual.txt
        pages = manfile.read().split('<p>')

        # Set the page index
        p_i = 0

        # draw the manual's window with the first page
        window = draw_manual_page(pages[p_i].splitlines(),'{0}/{1}'.format(p_i + 1, len(pages)))

        while True:
            wait_for = [tcod.KEY_KP4, tcod.KEY_KP6, tcod.KEY_LEFT, tcod.KEY_RIGHT]
            choice = menu_loop(wait_for = wait_for)

            tcod.console_delete(window) # Remove the old window on page change

            if choice is None:
                break

            if choice in [tcod.KEY_LEFT, tcod.KEY_KP4]:
                p_i -= 1
                if p_i < 0:
                    p_i = len(pages) - 1
            elif choice in [tcod.KEY_KP6, tcod.KEY_RIGHT]:
                p_i += 1
                if p_i >= len(pages):
                    p_i = 0

            window = draw_manual_page(pages[p_i].splitlines(),'{0}/{1}'.format(p_i + 1, len(pages)))


def draw_manual_page(page, pagecount):
    padding_x = 4
    padding_y = 4

    width = 82
    height = 60 #max(len(page), 55) + padding_y

    x = (cfg.SCREEN_WIDTH - width) // 2
    y = (cfg.SCREEN_HEIGHT - height) // 2

    # Create the window #
    window = tcod.console_new(width, height)
    window.caption = 'Manual'
    setup_console(window, borders=True, bordercolor=colors.darker_red)

    tcod.console_print(window,width - 12, 0, f'Page {pagecount}')
    tcod.console_print(window, 1, height - 1, '<Left/Right to navigate>')
    tcod.console_print(window, width - 15, height - 1, '<ESC to close>')

    offset_y = 2
    for p, paragraph in enumerate(page):
        tcod.console_print(window, 1, p + offset_y, paragraph)
        #window.draw_str( fg=colors.white, bg=None)
        # lines_wrapped = textwrap.wrap(paragraph, (width-padding_x//2))
        # for l, line in enumerate(lines_wrapped):
        # window.draw_str(1,p + offset_y, line, fg=colors.white, bg=None)
        # offset_y += 1

    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1, 1)
    tcod.console_flush()

    return window