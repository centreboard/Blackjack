import random

from deck import Deck
from player import Player


class RandomPlayer(Player):
    def __init__(self, name: str, limit=0.5):
        super().__init__(name)
        self.limit = limit

    def choose_take_card(self, cards: Deck, get_input=input):
        if random.random() < self.limit:
            self.take_card(cards)
        else:
            self.finished = True