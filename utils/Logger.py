import os
import sys
import logging


class Logger:
    DIR: str = 'logs'

    def __init__(self, name: str) -> None:
        if not os.path.exists(self.DIR):
            os.makedirs(self.DIR)

        formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        fileHandler = logging.FileHandler(self.DIR + '/' + name + '.log')
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(logging.INFO)
        consoleHandler.setFormatter(formatter)

        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger().addHandler(fileHandler)
        logging.getLogger().addHandler(consoleHandler)
