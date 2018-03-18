from typing import List

from card import Card
from deck import Deck


class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards: List[Card] = []
        self.finished = False
        self.wins = 0

    def __str__(self):
        return self.name

    def reset_hand(self):
        self.cards: List[Card] = []
        self.finished = False

    def take_card(self, deck: Deck):
        card = deck.random_card()
        self.cards.append(card)

    def choose_take_card(self, cards: Deck, get_input=input):
        take_card = get_input("Take card (y/N)? >").strip().lower()
        if take_card.startswith("y"):
            self.take_card(cards)
        elif take_card.startswith("n"):
            self.finished = True
        else:
            print("Invalid input")
            self.choose_take_card(cards, get_input)

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
