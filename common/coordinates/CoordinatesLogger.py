import logging
import matplotlib.pyplot as plt
from datetime import datetime
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from utils.Logger import Logger
from utils.Utils import createDirectory


class CoordinatesLogger:
    def __init__(self, coordinatesTransformer: CoordinatesTransformer,
                 directory: str) -> None:
        self.coordinatesTransformer = coordinatesTransformer
        self.directory = Logger.DIR + '/' + directory

        createDirectory(self.directory)

    def log(self, coordinates: list[Coordinate], tag: str, additional: str = None) -> str:
        name: str = self.__generateName(tag)

        if additional is None:
            createDirectory(self.directory + '/' + name)
            path: str = self.__getPath(name + '/' + name)
        else:
            path: str = self.__getPath(additional + '/' + name)

        self.__logAsPlot(coordinates, path)
        self.__logAsText(coordinates, name)

        return name

    def __generateName(self, tag: str) -> str:
        time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')

        return time + '_' + tag

    def __getPath(self, name: str) -> str:
        return self.directory + '/' + name + '.png'

    def __logAsPlot(self, coordinates: list[Coordinate], path: str) -> None:
        x, y, _ = self.coordinatesTransformer.separateToFloatLists(coordinates)

        fig, ax = plt.subplots()
        ax.grid(axis='both')
        ax.plot(x, y, label='xy', linewidth=4.0, c='tan', marker='o')
        ax.legend()
        fig.savefig(path)
        plt.close(fig)

    def __logAsText(self, coordinates: list[Coordinate], name: str) -> None:
        logging.debug('Plot "%s":' % name)

        for coordinate in coordinates:
            logging.debug('    x: %s, y: %s, angle: %s' % (coordinate.x, coordinate.y, coordinate.angle))
