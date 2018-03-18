import random
from typing import List, Union, Iterator


class Card:
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10,
              "A": 0}

    def __init__(self, symbol: Union[str, int], suit: str):
        self.suit = suit
        str_symbol = str(symbol)
        assert str_symbol in self.values, f"{str_symbol} not found in known card symbols"
        self.symbol = str_symbol

    def value(self, high=True) -> int:
        if self.symbol == "A":
            return 11 if high else 1
        return self.values[self.symbol]

    def __str__(self):
        return self.symbol + " " + self.suit


class Deck:
    def __init__(self, auto_refresh=True):
        self.auto_refresh = auto_refresh
        self._cards = self.new_deck()

    def __len__(self):
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
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
    def new_deck() -> List[Card]:
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


class Person:
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


def print_game_results(players: List[Person]):
    player_values = [(player, player.value()) for player in players]
    player_values.sort(key=lambda x: x[1], reverse=True)

    losers = [player for player, value in player_values if value > 21]
    eligible_players = [player for player, value in player_values if value <= 21]

    if eligible_players:
        winning_value = max((value for _, value in player_values if value <= 21))
        for player, _ in filter(lambda x: x[1] == winning_value, player_values):
            print(f"Winner: {player}")
            player.wins += 1
    else:
        print("No winner")
    for player in eligible_players:
        player.print_player()
    for player in losers:
        player.print_player()


def print_overall_results(players: List[Person]):
    for player in sorted(players, key=lambda x: x.wins, reverse=True):
        print(f"{player.name} - Wins: {player.wins}")


def game(players: List[Person], game_deck: Deck):
    print("====================")
    print("New game")
    print("====================")

    for player in players:
        player.reset_hand()

    for player in players:
        player.take_card(game_deck)
    for player in players:
        player.take_card(game_deck)

    current_players = [player for player in players if not player.finished and player.value() < 21]
    while current_players:
        for player in current_players:
            player.print_player()
            player.choose_take_card(game_deck)
        current_players = [player for player in players if not player.finished and player.value() < 21]

    print("====================")
    print_game_results(players)
    print("====================")
    print_overall_results(players)
    print("====================")


def main():
    deck = Deck()

    sam = Person("Sam")
    hannah = Person("Hannah")
    matt = Person("Matthew")
    players = [matt, hannah, sam]

    while deck:
        game(players, deck)


if __name__ == '__main__':
    main()
