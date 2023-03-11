#!/usr/bin/python

from utils.Logger import Logger
from common.commands.CommandsService import CommandsService
from common.coordinates.CoordinatesParser import CoordinatesParser
from common.coordinates.CoordinatesService import CoordinatesService
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.interpolation.CubicSplineService import CubicSplineService
from common.interpolation.InterpolateService import InterpolateService
from trainer.CommandsCreator import CommandsCreator
from trainer.TrainService import TrainService
from trainer.StanleyHelper import StanleyHelper
from trainer.StanleyController import StanleyController

Logger('train')


def getTrainService() -> TrainService:
    coordinatesParser = CoordinatesParser()

    coordinatesService = CoordinatesService()

    coordinatesLogger = CoordinatesLogger(
        coordinatesService,
        'train',
    )

    cubicSplineService = CubicSplineService()

    interpolateService = InterpolateService(
        coordinatesService,
        cubicSplineService,
    )

    stanleyHelper = StanleyHelper()

    stanleyController = StanleyController(
        stanleyHelper,
        interpolateService,
    )

    commandsCreator = CommandsCreator(
        coordinatesLogger,
        coordinatesService,
        stanleyController,
    )

    commandsService = CommandsService()

    return TrainService(
        coordinatesParser,
        coordinatesService,
        commandsCreator,
        commandsService,
    )


getTrainService().train()
