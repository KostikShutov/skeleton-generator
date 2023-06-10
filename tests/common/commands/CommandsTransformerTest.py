import unittest
from common.commands.Command import Command
from common.commands.CommandsTransformer import CommandsTransformer


class CommandsTransformerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.commandsTransformer = CommandsTransformer()

    def test_flatten(self) -> None:
        actual = self.commandsTransformer.flatten([])
        self.assertEqual([], actual)

        actual = self.commandsTransformer.flatten([
            Command(Command.MOVE, 1.2, 3.4),
            Command(Command.TURN, 5.6, 7.8),
        ])
        self.assertEqual([[1, 1.2, 3.4], [2, 5.6, 7.8]], actual)


if __name__ == '__main__':
    unittest.main()
