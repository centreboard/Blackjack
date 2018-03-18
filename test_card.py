from unittest import TestCase
from card import Card


class TestCard(TestCase):

    def test_card__unknown_int(self):
        def one():
            return Card(1, "Test")
        self.assertRaises(AssertionError, one)

    def test_card__unknown_symbol(self):
        def symbol():
            return Card("Sym", "Test")
        self.assertRaises(AssertionError, symbol)

    def test_value__integer_cards(self):
        for value in range(2, 11):
            with self.subTest(value=value):
                card = Card(value, "Test")
                self.assertEqual(value, card.value())

    def test_value__string_cards(self):
        for value in range(2, 11):
            with self.subTest(value=value):
                card = Card(str(value), "Test")
                self.assertEqual(value, card.value())

    def test_value__picture_cards(self):
        for symbol in ["J", "Q", "K"]:
            with self.subTest(value=symbol):
                card = Card(symbol, "Test")
                self.assertEqual(10, card.value())

    def test_value__ace_high(self):
        card = Card("A", "Test")
        self.assertEqual(11, card.value(high=True))

    def test_value__ace_low(self):
        card = Card("A", "Test")
        self.assertEqual(1, card.value(high=False))
