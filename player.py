from abc import ABC, abstractmethod
from typing import List

from card import Card
from deck import Deck


class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.cards: List[Card] = []
        self.finished = False
        self.wins = 0
        super().__init__()

    def __str__(self):
        return self.name

    def reset_hand(self):
        self.cards: List[Card] = []
        self.finished = False

    def take_card(self, deck: Deck):
        card = deck.random_card()
        self.cards.append(card)

    @abstractmethod
    def choose_take_card(self, cards: Deck, get_input=input):
        pass

    def print_hand(self):
        print(", ".join(str(card) for card in self.cards))

    def print_player(self):
        print(f"{self.name}: Total = {self.value()}")
        self.print_hand()

    def value(self) -> int:
        def get_value(cards, number_of_small=0):
            out = 0
            for i, card in enumerate(cards):
                out += card.value(i >= number_of_small)
            return out

        non_aces = [card for card in self.cards if card.symbol != "A"]
        aces = [card for card in self.cards if card.symbol == "A"]

        total_non_aces = get_value(non_aces)

        number_of_small_aces = 0
        total_aces = get_value(aces, number_of_small_aces)

        while total_non_aces + total_aces > 21:
            number_of_small_aces += 1
            if len(aces) >= number_of_small_aces:
                total_aces = get_value(aces, number_of_small_aces)
            else:
                break

        return total_non_aces + total_aces

