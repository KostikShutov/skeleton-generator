import unittest
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesService import CoordinatesService


class CoordinatesServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.coordinatesService = CoordinatesService()

    def test_separateToFloatLists(self) -> None:
        actual = self.coordinatesService.separateToFloatLists([])
        self.assertEqual(([], []), actual)

        actual = self.coordinatesService.separateToFloatLists([Coordinate(1.2, 3.4), Coordinate(5.6, 7.8)])
        self.assertEqual(([1.2, 5.6], [3.4, 7.8]), actual)

    def test_combineFromFloatLists(self) -> None:
        actual = self.coordinatesService.combineFromFloatLists([], [])
        self.assertEqual([], actual)

        actual = self.coordinatesService.combineFromFloatLists([1.2, 5.6], [3.4, 7.8])
        self.assertEqual(([Coordinate(1.2, 3.4), Coordinate(5.6, 7.8)]), actual)

    def test_splitToParts(self) -> None:
        actual = self.coordinatesService.splitToParts([])
        self.assertEqual([], actual)

        actual = self.coordinatesService.splitToParts([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
            Coordinate(13.14, 15.16),
            Coordinate(17.18, 19.20),
            Coordinate(21.22, 23.24),
        ])
        self.assertEqual([
            [Coordinate(0.0, 0.0), Coordinate(4.4, 4.4), Coordinate(7.9, 7.72)],
            [Coordinate(0.0, 0.0), Coordinate(3.5, 3.32), Coordinate(7.54, 7.36)],
            [Coordinate(0.0, 0.0), Coordinate(4.04, 4.04), Coordinate(8.08, 8.08)],
            [Coordinate(0.0, 0.0), Coordinate(4.04, 4.04), Coordinate(8.08, 8.08)],
        ], actual)

    def test_normalizeToZero(self) -> None:
        actual = self.coordinatesService.normalizeToZero([])
        self.assertEqual([], actual)

        actual = self.coordinatesService.normalizeToZero([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
        ])
        self.assertEqual([Coordinate(0.0, 0.0), Coordinate(4.4, 4.4), Coordinate(7.9, 7.72)], actual)

    def test_flattenWithRound(self) -> None:
        actual = self.coordinatesService.flattenWithRound([])
        self.assertEqual([], actual)

        actual = self.coordinatesService.flattenWithRound([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
        ])
        self.assertEqual([1.2, 3.4, 5.6, 7.8, 9.10, 11.12], actual)


if __name__ == '__main__':
    unittest.main()
