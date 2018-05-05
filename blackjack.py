import random
from typing import List

from deck import Deck
from player import Player, AIPlayer, RandomPlayer


def print_game_results(players: List[Player]):
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


def print_overall_results(players: List[Player]):
    for player in sorted(players, key=lambda x: x.wins, reverse=True):
        print(f"{player.name} - Wins: {player.wins}")


def game(players: List[Player], game_deck: Deck):
    print("====================")
    print("New game")
    print("====================")

    for player in players:
        player.reset_hand()

    # Start with two cards for each player
    for player in players:
        player.take_card(game_deck)
    for player in players:
        player.take_card(game_deck)

    # Choose to stick or twist
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

    sam = Player("Sam")
    hannah = RandomPlayer("Hannah", 0)
    matt = AIPlayer("Matthew", 16)
    players = [hannah, matt]

    #while deck:
    for _ in range(10000):
        random.shuffle(players)
        game(players, deck)


if __name__ == '__main__':
    main()
