#!/usr/bin/python

from utils.Logger import Logger
from common.commands.CommandsTransformer import CommandsTransformer
from common.coordinates.CoordinatesParser import CoordinatesParser
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.interpolation.CubicSplineService import CubicSplineService
from common.interpolation.InterpolateService import InterpolateService
from trainer.CommandsCreator import CommandsCreator
from trainer.TrainService import TrainService
from trainer.PredictiveHelper import PredictiveHelper
from trainer.PredictiveController import PredictiveController

Logger('train')


def getTrainService() -> TrainService:
    coordinatesParser = CoordinatesParser()

    coordinatesTransformer = CoordinatesTransformer()

    coordinatesLogger = CoordinatesLogger(
        coordinatesTransformer,
        'train',
    )

    cubicSplineService = CubicSplineService()

    interpolateService = InterpolateService(
        coordinatesTransformer,
        cubicSplineService,
    )

    predictiveHelper = PredictiveHelper()

    predictiveController = PredictiveController(
        predictiveHelper,
        interpolateService,
    )

    commandsCreator = CommandsCreator(
        coordinatesLogger,
        coordinatesTransformer,
        predictiveController,
    )

    commandsTransformer = CommandsTransformer()

    return TrainService(
        coordinatesParser,
        coordinatesTransformer,
        commandsCreator,
        commandsTransformer,
    )


getTrainService().train()
