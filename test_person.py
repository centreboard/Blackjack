from unittest import TestCase
from unittest.mock import MagicMock

from human_player import HumanPlayer
from deck import Deck
from card import Card


def fake_input(value):
    # noinspection PyUnusedLocal
    def _fake_input(prompt):
        return value

    return _fake_input


def fake_input_recursive(value, depth, second_value):
    called = 0

    # noinspection PyUnusedLocal
    def _fake_input(prompt):
        nonlocal called
        called += 1
        return value if called <= depth else second_value

    return _fake_input


def take_card_mock(deck, get_input):
    person = HumanPlayer("Sam")
    person.take_card = MagicMock()
    person.choose_take_card(deck, get_input)
    return person.take_card


class TestPerson(TestCase):
    def test_choose_take_card__yes(self):
        deck = [Card(3, "Test"), Card(2, "Test")]
        for input_return in ["y", "Y", "yes", "Yes", "YES", " y"]:
            with self.subTest(input_return=input_return):
                take_card_mock(deck, fake_input(input_return)).assert_called_once()

    def test_choose_take_card__wrong_then_yes(self):
        deck = [Card(3, "Test"), Card(2, "Test")]
        for input_return in ["", "maybe", "102938"]:
            with self.subTest(input_return=input_return):
                get_input = fake_input_recursive(input_return, 1, "y")
                take_card_mock(deck, get_input).assert_called_once()

    def test_choose_take_card__wrong_again_then_yes(self):
        deck = [Card(3, "Test"), Card(2, "Test")]
        for input_return in ["", "maybe", "102938"]:
            with self.subTest(input_return=input_return):
                get_input = fake_input_recursive(input_return, 10, "y")
                take_card_mock(deck, get_input).assert_called_once()

    def test_choose_take_card__wrong_then_no(self):
        deck = [Card(3, "Test"), Card(2, "Test")]
        for input_return in ["", "maybe", "102938"]:
            with self.subTest(input_return=input_return):
                get_input = fake_input_recursive(input_return, 1, "n")
                take_card_mock(deck, get_input).assert_not_called()

    def test_choose_take_card__no(self):
        deck = [Card(3, "Test"), Card(2, "Test")]
        for input_return in ["n", "N", "no", "NO", "n"]:
            with self.subTest(input_return=input_return):
                take_card_mock(deck, fake_input(input_return)).assert_not_called()

    def test_take_card__reduces_deck(self):
        deck = Deck()
        deck._cards = [Card(3, "Test"), Card(2, "Test")]
        person = HumanPlayer("Sam")

        person.take_card(deck)

        self.assertEqual(1, len(deck))

    def test_take_card__adds_to_hand(self):
        deck = Deck()
        deck._cards = [Card(3, "Test"), Card(2, "Test")]
        person = HumanPlayer("Sam")

        self.assertEqual(0, len(person.cards))
        person.take_card(deck)

        self.assertEqual(1, len(person.cards))

    def test_take_card__removes_card(self):
        deck = Deck()
        deck._cards = [Card(3, "Test"), Card(2, "Test")]
        person = HumanPlayer("Sam")

        person.take_card(deck)

        card = person.cards[0]
        self.assertNotIn(card, deck)

    def test_value__small_numbers(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(3, "Test"), Card(2, "Test")]

        self.assertEqual(5, person.value())

    def test_value__pictures(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("K", "Test"), Card("J", "Test")]

        self.assertEqual(20, person.value())

    def test_value__three_cards(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(3, "Test"), Card(2, "Test"), Card(8, "Test")]

        self.assertEqual(13, person.value())

    def test_value__over_21(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(9, "Test"), Card(9, "Test"), Card(8, "Test")]

        self.assertEqual(26, person.value())

    def test_value__ace_high_21(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(10, "Test"), Card("A", "Test")]

        self.assertEqual(21, person.value())

    def test_value__ace_high_under_21(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(7, "Test"), Card("A", "Test")]

        self.assertEqual(18, person.value())

    def test_value__ace_low_under_21(self):
        person = HumanPlayer("Sam")
        person.cards = [Card(7, "Test"), Card(8, "Test"), Card("A", "Test")]

        self.assertEqual(16, person.value())

    def test_value__ace_low_21(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("K", "Test"), Card("Q", "Test"), Card("A", "Test")]

        self.assertEqual(21, person.value())

    def test_value__two_aces(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("A", "Test"), Card("A", "Test")]

        self.assertEqual(12, person.value())

    def test_value__three_aces(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("A", "Test"), Card("A", "Test"), Card("A", "Test")]

        self.assertEqual(13, person.value())

    def test_value__four_aces(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("A", "Test"), Card("A", "Test"), Card("A", "Test"), Card("A", "Test")]

        self.assertEqual(14, person.value())

    def test_reset__empty_hand(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("A", "Test"), Card("A", "Test"), Card("A", "Test"), Card("A", "Test")]

        person.reset_hand()

        self.assertEqual([], person.cards)

    def test_reset__not_finished(self):
        person = HumanPlayer("Sam")
        person.finished = True

        person.reset_hand()

        self.assertFalse(person.finished)

    def test_reset__zero_value(self):
        person = HumanPlayer("Sam")
        person.cards = [Card("K", "Test"), Card("A", "Test")]

        person.reset_hand()

        self.assertEqual(0, person.value())
