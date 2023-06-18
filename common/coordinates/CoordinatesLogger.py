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

    def generateName(self, key: str) -> str:
        time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')

        return time + '_' + key

    def logAsPlot(self, coordinatesOld: list[Coordinate], coordinatesNew: list[Coordinate], name: str) -> None:
        coordinatesOldX, coordinatesOldY = self.coordinatesTransformer.separateToFloatLists(coordinatesOld)
        coordinatesNewX, coordinatesNewY = self.coordinatesTransformer.separateToFloatLists(coordinatesNew)

        fig, ax = plt.subplots()
        ax.grid(axis='both')
        ax.plot(coordinatesOldX, coordinatesOldY, label='Source', linewidth=4.0, c='red')
        ax.plot(coordinatesNewX, coordinatesNewY, label='Destination', linewidth=4.0, c='green')
        ax.legend()
        fig.gca().set_aspect('equal', adjustable='box')
        fig.savefig(self.__getPath(name))

    def logAsText(self, coordinates: list[Coordinate], title: str, name: str) -> None:
        logging.debug('%s "%s":' % (title, name))

        for coordinate in coordinates:
            logging.debug('    x: %s, y: %s, angle: %s' % (coordinate.x, coordinate.y, coordinate.angle))

    def __getPath(self, name: str) -> str:
        return self.directory + '/' + name + '.png'
