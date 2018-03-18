from unittest import TestCase

from blackjack import Deck


class TestDeckOfCards(TestCase):
    def test_deck_of_cards(self):
        deck = Deck()
        self.assertEqual(52, len(deck._cards))
