import logging
import os
import time


def initialize_logging(debugging=True, cleanup=True):
    """ configures logging """

    # configure logging
    formatting = '%(asctime)s | %(levelname)s |  %(funcName)s | %(message)s'
    log_file = f'logs/{time.strftime("%d.%m.%y %Hh%Mm")}.log'
    level = logging.DEBUG if debugging else logging.INFO
    logging.basicConfig(level=level, format=formatting)

    # disable all non-error messages if not debugging
    # if not debugging:
    #     logging.disable(logging.DEBUG)

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