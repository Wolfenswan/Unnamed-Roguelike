import re

import tcod

from config_files import cfg, colors
from gui.menus import menu_loop
from rendering.util_functions import setup_console, print_line, dynamic_wrap

def display_manual():
    """displays the game's manual"""

    width =  cfg.SCREEN_WIDTH
    height = cfg.SCREEN_HEIGHT
    padding_x = 4
    break_point = 4 # distance to page end at which to break the page

    with open('resources/manual.txt') as manfile:
        pages = [dynamic_wrap(page, max_width=width - padding_x) for page in
                        re.split(r'<page\s\d>', manfile.read()) if len(page) > 0]
        for page in pages:
            if page[0] == ' ': del page[0] # cleanup required as re.split creates an empty string for each match which translates to an empty line at the beginning of each page from the second on

    p_i = 0  # page index
    line = 0 # what line to display

    while True:
        window = draw_manual_page(pages, p_i, line, width, height, break_point)

        wait_for = [tcod.KEY_KP4, tcod.KEY_KP6, tcod.KEY_KP2, tcod.KEY_KP8, tcod.KEY_LEFT, tcod.KEY_RIGHT, tcod.KEY_UP, tcod.KEY_DOWN] # todo scrolling up/down
        choice = menu_loop(wait_for = wait_for)

        tcod.console_delete(window) # Remove the old window on page change

        if choice is None:
            break

        if choice in [tcod.KEY_LEFT, tcod.KEY_KP4]:
            p_i -= 1
            line = 0
            if p_i < 0:
                p_i = len(pages) - 1
        elif choice in [tcod.KEY_KP6, tcod.KEY_RIGHT]:
            p_i += 1
            line = 0
            if p_i >= len(pages):
                p_i = 0
        elif choice in [tcod.KEY_DOWN, tcod.KEY_KP2]:
            if (len(pages[p_i])-line > height - break_point):
                line += 1
        elif choice in [tcod.KEY_UP, tcod.KEY_KP8]:
            line = max(0,line - 1)

def draw_manual_page(pages, index, line, width, height, break_point):

    page = pages[index]
    page_counter = f'Page {index+1}/{len(pages)}'

    x = 0
    y = 0
    offset = 1 # ensures that strings aren't drawn on the borders

    # Create the window #
    window = tcod.console_new(width, height)
    window.caption = 'Manual'
    setup_console(window, borders=True, bordercolor=colors.darker_red)

    print_line(window, width - len(page_counter) - offset, 0, page_counter)
    print_line(window, offset, height - offset, '<Directional keys to navigate>')
    print_line(window, width - 15, height - offset, '<ESC to close>')

    for line_count, paragraph in enumerate(page[line:]):
        line_count += offset
        print_line(window, 1, line_count, paragraph)
        if line_count + break_point > height:
            breaker = '# MORE #'
            print_line(window,width//2-len(breaker),line_count+1,breaker,color=colors.grey)
            break

    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1, 1)
    tcod.console_flush()

    return window