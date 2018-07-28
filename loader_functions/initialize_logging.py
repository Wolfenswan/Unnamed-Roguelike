import logging
import os
import time

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
    rootLogger = logging.getLogger()

    # file output
    logFormatter = logging.Formatter(formatting)
    fileHandler = logging.FileHandler(f'{format(log_file)}')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

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