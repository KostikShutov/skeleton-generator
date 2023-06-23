import unittest
from common.coordinates.Coordinate import Coordinate
from common.coordinates.CoordinatesTransformer import CoordinatesTransformer


class CoordinatesTransformerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.coordinatesTransformer = CoordinatesTransformer()

    def test_separateToFloatLists(self) -> None:
        actual = self.coordinatesTransformer.separateToFloatLists([])
        self.assertEqual(([], [], []), actual)

        actual = self.coordinatesTransformer.separateToFloatLists([
            Coordinate(1.2, 3.4, 5.6),
            Coordinate(7.8, 9.10, 11.12),
        ])
        self.assertEqual((
            [1.2, 7.8],
            [3.4, 9.10],
            [5.6, 11.12],
        ), actual)

    def test_combineFromFloatLists(self) -> None:
        actual = self.coordinatesTransformer.combineFromFloatLists([], [])
        self.assertEqual([], actual)

        actual = self.coordinatesTransformer.combineFromFloatLists([], [], [])
        self.assertEqual([], actual)

        actual = self.coordinatesTransformer.combineFromFloatLists(
            [1.2, 5.6],
            [3.4, 7.8],
        )
        self.assertEqual(([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
        ]), actual)

        actual = self.coordinatesTransformer.combineFromFloatLists(
            [1.2, 7.8],
            [3.4, 9.10],
            [5.6, 11.12]
        )
        self.assertEqual(([
            Coordinate(1.2, 3.4, 5.6),
            Coordinate(7.8, 9.10, 11.12),
        ]), actual)

    def test_splitToParts(self) -> None:
        actual = self.coordinatesTransformer.splitToParts([])
        self.assertEqual([], actual)

        actual = self.coordinatesTransformer.splitToParts([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
            Coordinate(13.14, 15.16),
            Coordinate(17.18, 19.20),
            Coordinate(21.22, 23.24),
        ])
        self.assertEqual([
            [Coordinate(1.2, 3.4), Coordinate(5.6, 7.8), Coordinate(9.10, 11.12)],
            [Coordinate(5.6, 7.8), Coordinate(9.10, 11.12), Coordinate(13.14, 15.16)],
            [Coordinate(9.10, 11.12), Coordinate(13.14, 15.16), Coordinate(17.18, 19.20)],
            [Coordinate(13.14, 15.16), Coordinate(17.18, 19.20), Coordinate(21.22, 23.24)],
        ], actual)

    def test_normalizeToZero(self) -> None:
        actual = self.coordinatesTransformer.normalizeToZero([])
        self.assertEqual([], actual)

        actual = self.coordinatesTransformer.normalizeToZero([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
        ])
        self.assertEqual([Coordinate(4.4, 4.4), Coordinate(7.9, 7.72)], actual)

    def test_flatten(self) -> None:
        actual = self.coordinatesTransformer.flatten([])
        self.assertEqual([], actual)

        actual = self.coordinatesTransformer.flatten([
            Coordinate(1.2, 3.4),
            Coordinate(5.6, 7.8),
            Coordinate(9.10, 11.12),
        ])
        self.assertEqual([[1.2, 3.4], [5.6, 7.8], [9.10, 11.12]], actual)


if __name__ == '__main__':
    unittest.main()
