from unittest import TestCase
from unittest.mock import patch, MagicMock

from blackjack import print_game_results
from player import Player
from card import Card


# noinspection PyUnusedLocal
@patch('blackjack.print')
class TestPrintResults(TestCase):
    def test_print_results__one_person__is_winner(self, mock_print: MagicMock):
        person = Player("Matthew")
        person.print_player = MagicMock()
        person.cards = []

        print_game_results([person])

        mock_print.assert_called_once_with("Winner: Matthew")

    def test_print_results__one_person_empty_hand(self, mock_print: MagicMock):
        person = Player("Matthew")
        person.print_player = MagicMock()
        print_game_results([person])

        person.print_player.assert_called_once()

    def test_print_results__one_person_low_hand(self, mock_print: MagicMock):
        person = Player("Matthew")
        person.print_player = MagicMock()
        person.cards = [Card(2, "Test")]
        print_game_results([person])

        person.print_player.assert_called_once()

    def test_print_results__one_person_high_hand(self, mock_print: MagicMock):
        person = Player("Matthew")
        person.print_player = MagicMock()
        person.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]
        print_game_results([person])

        person.print_player.assert_called_once()

    def test_print_results__people_print_person_called_once(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(2, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(5, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)
        for player in players:
            with self.subTest(player=player.name):
                # noinspection PyUnresolvedReferences
                player.print_player.assert_called_once()

    def test_print_results__people_single_winner(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(2, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(5, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)

        mock_print.assert_called_once_with("Winner: Sam")

    def test_print_results__people_joint_winner(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(2, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(10, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)

        mock_print.assert_any_call("Winner: Sam")
        mock_print.assert_any_call("Winner: Hannah")
        self.assertRaises(AssertionError, lambda: mock_print.assert_any_call("Winner: Matthew"))

    def test_print_results__people_single_winner_one_over(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(5, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)

        mock_print.assert_called_once_with("Winner: Sam")

    def test_print_results__people_joint_winner_one_over(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(10, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)

        mock_print.assert_any_call("Winner: Sam")
        mock_print.assert_any_call("Winner: Hannah")
        self.assertRaises(AssertionError, lambda: mock_print.assert_any_call("Winner: Matthew"))

    def test_print_results__people_no_winner(self, mock_print: MagicMock):
        matt = Player("Matthew")
        matt.print_player = MagicMock()
        matt.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]

        sam = Player("Sam")
        sam.print_player = MagicMock()
        sam.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]

        hannah = Player("Hannah")
        hannah.print_player = MagicMock()
        hannah.cards = [Card(10, "Test"), Card(10, "Test"), Card(10, "Test")]

        players = [matt, sam, hannah]
        print_game_results(players)

        self.assertRaises(AssertionError, lambda: mock_print.assert_any_call("Winner: Matthew"))
        self.assertRaises(AssertionError, lambda: mock_print.assert_any_call("Winner: Sam"))
        self.assertRaises(AssertionError, lambda: mock_print.assert_any_call("Winner: Hannah"))
        mock_print.assert_called_once_with("No winner")
