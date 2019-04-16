from deck import Deck
from player import Player


class AiPlayer(Player):
    def __init__(self, name: str, limit=15):
        super().__init__(name)
        self.limit = limit

    def choose_take_card(self, cards: Deck, get_input=input):
        if self.value() <= self.limit:
            self.take_card(cards)
        else:
            self.finished = True