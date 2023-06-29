import sys
import logging
from utils.Utils import createDirectory


class Logger:
    DIR: str = 'logs'

    def __init__(self, name: str) -> None:
        createDirectory(self.DIR)

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
