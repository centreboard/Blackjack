import random
from collections import deque

from deck import Deck
from player import Player, AiPlayer, RandomPlayer


def get_game_results(players):
    player_values = [(player, player.value()) for player in players]
    player_values.sort(key=lambda x: x[1], reverse=True)

    losers = [player for player, value in player_values if value > 21]
    eligible_players = [player for player, value in player_values if value <= 21]
    winners = []
    if eligible_players:
        winning_value = max((value for _, value in player_values if value <= 21))
        for player, _ in filter(lambda x: x[1] == winning_value, player_values):
            winners.append(player)
            player.wins += 1
    return winners, eligible_players, losers


def print_game_results(players):
    winners, eligible_players, losers = get_game_results(players)

    if winners:
        for player in winners:
            print("Winner: " + player.name)
    else:
        print("No winner")
    for player in eligible_players:
        player.print_player()
    for player in losers:
        player.print_player()


def print_overall_results(players):
    for player in sorted(players, key=lambda x: x.wins, reverse=True):
        print("{0} - Wins: {1}".format(player.name, player.wins))


def game(players, game_deck: Deck, always_print=True):
    if always_print:
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
            if always_print:
                player.print_player()
            player.choose_take_card(game_deck)
        current_players = [player for player in players if not player.finished and player.value() < 21]

    if always_print:
        print("====================")
        print_game_results(players)
        print("====================")
        print_overall_results(players)
        print("====================")
    else:
        get_game_results(players)


def main():
    deck = Deck(True)

    sam = Player("Sam")
    hannah = AiPlayer("Hannah", 16)
    matt = Player("Matthew")
    players = deque([matt, hannah, sam])

    # while deck:
    for _ in range(100000):
        game(players, deck, True)
        players.rotate(1)
    print("====================")
    print_overall_results(players)
    print("====================")


if __name__ == '__main__':
    main()
