import random

from card import Card


class Deck:
    def __init__(self, auto_refresh=True):
        self.auto_refresh = auto_refresh
        self._cards = self.new_deck()

    def __len__(self):
        return len(self._cards)

    def __iter__(self):
        return self._cards.__iter__()

    def random_card(self) -> Card:
        if not self._cards:
            if self.auto_refresh:
                self._cards = self.new_deck()
            else:
                raise Exception("Out of cards")
        card = random.choice(self._cards)
        self._cards.remove(card)
        return card

    @staticmethod
    def new_deck():
        """
        A new deck of 52 cards
        """
        cards = []
        for suit in ["♠", "♥", "♦", "♣"]:
            for symbol in range(2, 11):
                cards.append(Card(symbol, suit))
            for symbol in ["J", "Q", "K", "A"]:
                cards.append(Card(symbol, suit))
        return cards
