import unittest
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesParser import CoordinatesParser


class CoordinatesParserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.coordinatesParser = CoordinatesParser()

    def test_parse(self) -> None:
        actual = self.coordinatesParser.parse([])
        self.assertEqual([], actual)

        actual = self.coordinatesParser.parse([{'x': 1.2, 'y': 3.4}, {'x': 5.6, 'y': 7.8}])
        self.assertEqual([Coordinate(1.2, 3.4), Coordinate(5.6, 7.8)], actual)


if __name__ == '__main__':
    unittest.main()
