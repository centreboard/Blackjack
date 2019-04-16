from deck import Deck
from player import Player


class HumanPlayer(Player):
    def choose_take_card(self, cards: Deck, get_input=input):
        take_card = get_input("Take card (y/N)? >").strip().lower()
        if take_card.startswith("y"):
            self.take_card(cards)
        elif take_card.startswith("n"):
            self.finished = True
        else:
            print("Invalid input")
            self.choose_take_card(cards, get_input)