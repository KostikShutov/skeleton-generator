import os
import matplotlib.pyplot as plt
from datetime import datetime
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesService import CoordinatesService


class CoordinatesLogger:
    def __init__(self, coordinatesService: CoordinatesService,
                 directory: str) -> None:
        self.coordinatesService = coordinatesService
        self.directory = 'logs/' + directory

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def log(self, coordinatesOld: list[Coordinate], coordinatesNew: list[Coordinate], chart: str) -> None:
        coordinatesOldX, coordinatesOldY = self.coordinatesService.separateToFloatLists(coordinatesOld)
        coordinatesNewX, coordinatesNewY = self.coordinatesService.separateToFloatLists(coordinatesNew)

        fig, ax = plt.subplots()
        ax.grid(axis='both')
        ax.plot(coordinatesOldX, coordinatesOldY, label='Source', linewidth=4.0, c='red')
        ax.plot(coordinatesNewX, coordinatesNewY, label='Destination', linewidth=4.0, c='green')
        ax.legend()
        fig.gca().set_aspect('equal', adjustable='box')
        fig.savefig(self.__getPath(chart))

    def __getPath(self, chart: str) -> str:
        time: str = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

        return self.directory + '/' + time + '_' + chart + '.png'
