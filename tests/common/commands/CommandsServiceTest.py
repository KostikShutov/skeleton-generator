import unittest
from common.commands.Command import Command
from common.commands.CommandsService import CommandsService


class CommandsServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.commandsService = CommandsService()

    def test_flattenWithRound(self) -> None:
        actual = self.commandsService.flattenWithRound(Command(1.2, 3.4))
        self.assertEqual([1.2, 3.4], actual)


if __name__ == '__main__':
    unittest.main()
