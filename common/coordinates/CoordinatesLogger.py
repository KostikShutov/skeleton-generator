import os
import logging
import matplotlib.pyplot as plt
from datetime import datetime
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from utils.Logger import Logger


class CoordinatesLogger:
    def __init__(self, coordinatesTransformer: CoordinatesTransformer,
                 directory: str) -> None:
        self.coordinatesTransformer = coordinatesTransformer
        self.directory = Logger.DIR + '/' + directory

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def log(self, coordinates: list[Coordinate], key: str) -> None:
        name: str = self.__generateName(key)

        self.__logAsPlot(coordinates, name)
        self.__logAsText(coordinates, name)

    def __generateName(self, key: str) -> str:
        time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')

        return time + '_' + key

    def __logAsPlot(self, coordinates: list[Coordinate], name: str) -> None:
        x, y, _ = self.coordinatesTransformer.separateToFloatLists(coordinates)

        fig, ax = plt.subplots()
        ax.grid(axis='both')
        ax.plot(x, y, label='xy', linewidth=4.0, c='tan', marker='o')
        ax.legend()
        fig.gca().set_aspect('equal', adjustable='box')
        fig.savefig(self.__getPath(name))
        plt.close(fig)

    def __logAsText(self, coordinates: list[Coordinate], name: str) -> None:
        logging.debug('Plot "%s":' % name)

        for coordinate in coordinates:
            logging.debug('    x: %s, y: %s, angle: %s' % (coordinate.x, coordinate.y, coordinate.angle))

    def __getPath(self, name: str) -> str:
        return self.directory + '/' + name + '.png'
