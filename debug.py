import logging
import os
import time
from functools import wraps

from gui.menus import options_menu
from gui.messages import Message, MessageType, MessageCategory


def initialize_logging(debugging=True, cleanup=True):
    """ configures logging """

    # configure logging
    formatting = '%(asctime)s | %(levelname)s |  %(funcName)s | %(message)s'
    log_file = f'logs/{time.strftime("%d.%m.%y %Hh%Mm")}.log'
    logging.basicConfig(level=logging.DEBUG, format=formatting)

    # disable all non-error messages if not debugging
    if not debugging:
        logging.disable(logging.DEBUG)

    # setup output streams
    rootlogger = logging.getLogger()

    # file output
    logformatter = logging.Formatter(formatting)
    filehandler = logging.FileHandler(f'{format(log_file)}')
    filehandler.setFormatter(logformatter)
    rootlogger.addHandler(filehandler)

    if cleanup:
        last_logs_to_keep = 3
        folder = 'logs/'
        for root, dirs, files in os.walk(folder):
            for file in files[:-last_logs_to_keep]:
                os.remove(os.path.join(root, file))

    # terminal output
    # consoleHandler = logging.StreamHandler()
    # consoleHandler.setFormatter(logFormatter)
    # rootLogger.addHandler(consoleHandler)


def debug_timer(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        logging.debug("{} ran in {}s".format(function.__name__, round(end - start, 2)))
        return result

    return wrapper


def debug_menu(game):
    choice = options_menu('Debug Menu', 'Select Debug Option:',
                          ['Show full map', 'Invincible Player', 'Entity Debug Information', 'Spawn Monster (Not implemented!)', 'Spawn Item (Not implemented!)'], sort_by=1,
                          cancel_with_escape=True)
    if choice == 0:
        game.debug['map'] = not game.debug['map']
        Message(f'Map visibility set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 1:
        game.debug['invin'] = not game.debug['invin']
        Message(f'Player Invincibility set to {game.debug["invin"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)
    elif choice == 2:
        game.debug['ent_info'] = not game.debug['ent_info']
        Message(f'Entity Debug Information set to {game.debug["map"]}', type=MessageType.GAME,
                category=MessageCategory.OBSERVATION).add_to_log(game)