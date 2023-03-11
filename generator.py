#!/usr/bin/python

from utils.Logger import Logger
from flask import Flask, request
from flask_cors import CORS, cross_origin
from common.coordinates.CoordinatesParser import CoordinatesParser
from common.coordinates.CoordinatesLogger import CoordinatesLogger
from common.coordinates.CoordinatesService import CoordinatesService
from common.interpolation.CubicSplineService import CubicSplineService
from common.interpolation.InterpolateService import InterpolateService
from predictor.CommandsPredictor import CommandsPredictor
from predictor.PredictService import PredictService

Logger('generator')

app = Flask(__name__)
cors = CORS(app)


def getPredictService() -> PredictService:
    coordinatesService = CoordinatesService()

    coordinatesLogger = CoordinatesLogger(
        coordinatesService,
        'generator',
    )

    cubicSplineService = CubicSplineService()

    interpolateService = InterpolateService(
        coordinatesService,
        cubicSplineService,
    )

    commandsPredictor = CommandsPredictor(
        coordinatesLogger,
        coordinatesService,
        interpolateService,
    )

    return PredictService(
        commandsPredictor,
    )


coordinatesParser = CoordinatesParser()
predictService = getPredictService()


@app.route('/generate', methods=['POST'])
@cross_origin()
def generate():
    data = request.get_json(silent=True)
    coordinates = coordinatesParser.parse(data)

    return predictService.predict(coordinates)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
