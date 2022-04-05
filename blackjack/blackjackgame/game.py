#!/usr/bin/env python3
# Bilal El-haghassan
# CPSC 386-04
# 2022-04-04
# bilalelhaghassan@csu.fullerton.edu
# @belhaghassan
#
# Lab 03-03
#
# This is BlackJackGame, a game of Cards and money
#

"""This is a game of BlackJackGame with 1 - 4 players"""

from random import randint
import time
import os
from blackjackgame import cards
from blackjackgame import player as Player


class BlackJackGame:
    """Game Class for Blackjack"""

    def __init__(self):
        self._num_of_players = 0
        self._dealer = Player.Dealer("Dealer", randint(100, 1000))
        self._records = None
        self._players = {}
        self._ai_players = ["Optimus Prime", "Megatron", "Zora", "Skynet"]
        self._game_is_not_over = True
        self.line = (
            "\t"
            "******************************************************************"
            "\n"
        )

    def new_hand(self, player):
        """Print out of current player and Dealers hand"""
        time.sleep(0.5)
        player.add_score()
        self._dealer.add_score()
        self.hand(self._dealer)
        time.sleep(1)
        self.hand(player)
        time.sleep(1)

    def hand(self, player):
        """Graphical representation of player hand"""

        suits = {"Clubs": "♣", "Hearts": "♥", "Spades": "♠", "Diamonds": "♦"}
        rank = {"Jack": "J", "Queen": "Q", "King": "K", "Ace": "A"}

        time.sleep(1)
        cards_in_hand = []
        print(self.line)
        if player.is_split:
            print(f"\t{player.name}'s Hand:")
            for idx, hand in enumerate(player.cards()):
                print(f"\n\tHand {idx + 1}")
                for card in hand:
                    if card.rank in rank:
                        rnk = rank[card.rank]
                    else:
                        rnk = card.rank
                    suit = suits[card.suit]
                    cards_in_hand.append(cards.card_template(rnk, suit))
                card_list = list(range(len(cards_in_hand)))
                lines = [cards_in_hand[i].splitlines() for i in card_list]
                for lis in zip(*lines):
                    print(*lis, sep="")
                score = player.score2 if idx == 1 else player.score
                print(
                    f"\tCurrent Score: {score}\n"
                    f"\tCurrent Wager: $"
                    f"{self._players[player][f'wager{idx + 1}']}"
                )
                time.sleep(1)
                cards_in_hand.clear()

        else:
            print(f"\t{player.name}'s Hand:")
            for idx, card in enumerate(player.cards()):
                if card.rank in rank:
                    rnk = rank[card.rank]
                else:
                    rnk = card.rank
                suit = suits[card.suit]
                if (
                    player.name == "Dealer"
                    and idx == 1
                    and player.hidden
                ):
                    template = (
                        "\t ___________\n"
                        "\t|           |\n"
                        "\t|     _     |\n"
                        "\t|   /   \\   |\n"
                        "\t|       /   |\n"
                        "\t|     |     |\n"
                        "\t|     .     |\n"
                        "\t|           |\n"
                        "\t|___________|\n\n"
                    )
                else:
                    template = cards.card_template(rnk, suit)
                cards_in_hand.append(template)
            card_list = list(range(len(cards_in_hand)))
            lines = [cards_in_hand[i].splitlines() for i in card_list]
            for lis in zip(*lines):
                print(*lis, sep="")
            print(f"\tCurrent Score: {player.score}\n")
        print(self.line)

        time.sleep(1)

    def player_input(self, num_of_players):
        """Take in and save player names"""

        if os.path.exists("players.pkl"):
            self._records = Player.from_file("players.pkl")
        else:
            Player.to_file("players.pkl", {})
            self._records = Player.from_file("players.pkl")

        for plyr in range(num_of_players):
            player_name = input(f"\n\tPlayer {plyr + 1}'s name: ")
            player_user_id = input(f"\t{player_name}'s user ID: ")
            player_exists = False

            returned_player = None
            for veteran in self._records:
                if veteran.name == player_name and veteran.identifier == player_user_id:
                    self._players[veteran] = {}
                    returned_player = veteran
                    player_exists = True
            if returned_player is not None:
                self._records.pop(returned_player)
            if player_exists is False:
                self._players[Player.Player(player_name, player_user_id)] = {}

        if num_of_players < 2:
            for _ in range(2 - num_of_players):
                ai_name = self._ai_players.pop(_)
                ai_player = Player.ComputerPlayer(ai_name, _)
                player_exists = False

                returned_player = None
                for veteran in self._records:
                    if (
                        veteran.name == ai_name 
                        and veteran.identifier == _
                    ):
                        self._players[veteran] = {}
                        returned_player = veteran
                        player_exists = True
                if returned_player is not None:
                    self._records.pop(returned_player)
                if player_exists is False:
                    self._players[ai_player] = {}

                self._num_of_players += 1
                time.sleep(0.5)
                print(f"\n\tAI {ai_name} joined the game\n\n")

        time.sleep(1)

    def hit_or_stay(self, players, hand):
        """Function to deal card or stay"""
        while players.hit_or_stand():
            time.sleep(1)
            players.add_card(self._dealer.deal, hand)
            players.add_score()
            self.new_hand(players)
            time.sleep(0)
            if players.score > 21:
                if players.name != "Dealer":
                    print(
                        f"\t{players.name} loses $"
                        f"\t{self._players[players][f'wager{hand + 1}']}" 
                        "wager."
                    )
                break

    def check_winners(self, player, hand, wager):
        """Check if player beat dealer"""

        wage = self._players[player][wager]
        if hand < 22:
            if self._dealer.score == hand:
                print("\tDRAW - No winnings or losses.\n")
                player.add_balance(wage)

            elif self._dealer.score > 22 or hand > self._dealer.score:

                player.add_balance(wage * 2)
                print(
                    "\t\t\t\t******WINNER******\n\n"
                    f"\t{player.name} wins ${wage} wager\n"
                )
                print(f"\tNew Balance after winning: ${player.get_balance}\n\n")
                self.line
            else:
                print(
                    f"\t{player.name} loses ${wage} wager\n"
                    f"\tNew Balance after losing: ${player.get_balance}\n\n"
                )
                self.line
        else:
            print(
                f"\t{player.name} loses ${wage} wager\n"
                f"\tNew Balance after losing: ${player.get_balance}\n\n"
            )
            self.line

        if "insurance" in self._players[player] and self._dealer.score == 21:
            player.add_balance(self._players[player]["insurance"] * 2)
            print(
                f"{self.line}"
                "\t\t\t\t******WINNER******\n"
                f"{player} wins insurance wager of $",
                f"{self._players[player]['insurance']}\n\n" f"{self.line}",
            )

    def game_round(self):
        # Player's opportunity to split, double down or buy insurance
        for players in self._players:
            if self._players[players]["wager1"] > 0:
                if players.get_balance < 1:
                    players.top_up()
                self.new_hand(players)
                if (
                    cards.card_value(self._dealer.cards()[0]) == 10
                    or self._dealer.cards()[0].rank == "Ace"
                ):

                    insurance = input(
                        f"\tWould {players.name} like to buy insurance?"
                        " ('yes'/'y' or 'no'/'n'): "
                    )
                    if insurance in ["y", "yes"] and players.get_balance > 0:
                        print(f"\n\t{players.name} buys insurance!")
                        self._players[players][
                            "insurance"
                        ] = players.place_bet()
                        players.wage(self._players[players]["insurance"])

                # Check if player can split
                if (
                    # players.cards()[0].rank == players.cards()[1].rank and 
                    (self._players[players]["wager1"] * 2) 
                    <= players.get_balance
                ):
                    split = input(
                        "\tWould you like to split? ('yes'/'y' or 'no'/'n'): "
                    )
                    if split in ["y", "yes"]:
                        players.split()
                        players.add_card(self._dealer.deal, 0)
                        players.add_card(self._dealer.deal, 1)
                        self._players[players]["wager2"] = self._players[
                            players
                        ]["wager1"]
                        players.wage(self._players[players]["wager2"])
                        self.new_hand(players)

                # Check if player wants to double down
                if self._players[players]["wager1"] * 2 <= players.get_balance:
                    self.double_down(players)

                if players.is_split:
                    if players.double_down:
                        if players.double_down2 is False:
                            print("\n\tFor hand 2:")
                            self.hit_or_stay(players, 1)
                    elif players.double_down2:
                        print("\n\tFor hand 1:")
                        self.hit_or_stay(players, 0)
                    else:
                        print("\n\tFor hand 1:")
                        self.hit_or_stay(players, 0)
                        print("\n\tFor hand 2:")
                        self.hit_or_stay(players, 1)
                elif players.double_down is False:
                    self.hit_or_stay(players, 0)

    def run(self):
        """Main BlackJack run function"""

        welcome = """
         _______________________________________________________________
        |                                                               |
        |    ♣  ♥  ♠  ♦                                    ♣  ♥  ♠  ♦   |
        |                           WELCOME                             |
        |                             TO                                |
        |                                                               |
        |         ___   __            __       __            __         |
        |        / _ ) / /___ _ ____ / /__ __ / /___ _ ____ / /__       |
        |       / _  |/ // _ `// __//  '_// // // _ `// __//  '_/       |
        |      /____//_/ \\_,_/ \\__//_/\\_\\ \\___/ \\_,_/ \\__//_/\\_\\  \t|
        |                                                               |
        |                                                               |
        |                         ____ ___________                      |
        |                        |    |           |                     |
        |                        | J♠ |A♠         |                     |
        |                        |    |           |                     |
        |                        |    |     ♠     |                     |
        |                        |    |           |                     |
        |                        |    |        A♠ |                     |
        |                        |____|___________|                     |
        |                                                               |
        |                                                               |
        |    ♣  ♥  ♠  ♦                                    ♣  ♥  ♠  ♦   |
        |_______________________________________________________________|
        """
        print("\t\t", welcome)
        print(self.line)

        # Ask user how many players are going to play?
        while True:
            print("\tHow many players: [1 - 4]? ", end=" ")
            self._num_of_players = int(f"{input()}")
            if self._num_of_players <= 4 and self._num_of_players >= 1:
                break
            print("\tInvalid number of players. Try again.\n")

        self.player_input(self._num_of_players)

        dealer = self._dealer

        while self._game_is_not_over:

            # Players asked to place bet
            for plyr in self._players:
                print(f"\t{plyr.name}'s Balance: {plyr.get_balance}")
                self._players[plyr] = {"wager1": plyr.place_bet()}
                plyr.wage(self._players[plyr]["wager1"])
                print()

            # Deal to two cards to each player
            for _ in range(2):
                for plyr in self._players:
                    if self._players[plyr]["wager1"] > 0:
                        plyr.add_card(dealer.deal)
                dealer.add_card(dealer.deal)

            self.game_round()

            # Dealers move
            dealer.show
            dealer.add_score()
            self.line
            print("\tDealers Turn\n")
            self.hand(dealer)
            time.sleep(1)
            print(f"\tDealer's score: {dealer.score}")
            self.hit_or_stay(dealer, dealer.cards()[0])

            # Check which players win
            for player in self._players:
                self.new_hand(player)
                if player.score2:
                    self.check_winners(player, player.score, "wager1")
                    self.check_winners(player, player.score2, "wager2")
                    del self._players[player]["wager2"]
                else:
                    self.check_winners(player, player.score, "wager1")
                player.reset
                del self._players[player]["wager1"]
            dealer.reset
            dealer.hide

            self._players.update(self._records)
            Player.to_file("players.pkl", self._players)

            print(self.line)

            if input(
                f"\n\tPlayer {list(self._players)[0].name} would you like to "
                "play again? \n\t('yes'/'y' or 'no'/'n'): "
            ) in ["y", "yes"]:
                print(
                    "\n",
                    self.line,
                    self.line,
                    "\n\t\t\t\tANOTHER ROUND!\n\n",
                    self.line,
                    self.line,
                )
            else:
                self._game_is_not_over = False
                print(
                    "\n",
                    self.line,
                    self.line,
                    "\n\t\t\t\tGAME OVER\n\n",
                    self.line,
                    self.line,
                )

    def double_down(self, player):
        """Function to double down on a players wager"""

        double_down = input(
            "\tWould you like to double down? ('yes'/'y' or 'no'/'n'): "
        )
        if double_down in ["y", "yes"]:
            if player.is_split:
                if self._players[player]["wager1"] * 4 < player.get_balance:
                    choice = input(
                        "\n\tWhich hand would you like to double down on?"
                        "\n\t- ANYKEY for first"
                        "\n\t- '2' for second hand"
                        "\n\t- 'both' for both hands"
                        "\n\t"
                    )
                else:
                    choice = input(
                        "\tWhich hand would you like to double down on?"
                        "\n\t- ANYKEY for first"
                        "\n\t- '2' for second hand"
                        "\n\t"
                    )
                if (
                    choice == "both"
                    and self._players[player]["wager1"] * 4 < player.get_balance
                ):
                    player.add_card(self._dealer.deal)
                    player.add_card(self._dealer.deal, 1)
                    player.double_down = True
                    player.double_down2 = True
                    player.wage(self._players[player]["wager1"] * 2)
                    self._players[player]["wager2"] = (
                        self._players[player]["wager1"] * 2
                    )
                    self._players[player]["wager1"] = (
                        self._players[player]["wager1"] * 2
                    )
                    print(f"\n\t{player.name} doubled down on BOTH hands!\n")
                elif choice == "2":
                    print(f"\n\t{player.name} will double down on 2nd hand!\n")
                    player.add_card(self._dealer.deal, 1)
                    player.double_down2 = True
                    player.wage(self._players[player]["wager1"])
                    self._players[player]["wager2"] = (
                        self._players[player]["wager1"] * 2
                    )
                else:
                    print(f"\n\t{player.name} will double down on 1st hand!\n")
                    player.add_card(self._dealer.deal)
                    player.double_down = True
                    player.wage(self._players[player]["wager1"])
                    self._players[player]["wager1"] = (
                        self._players[player]["wager1"] * 2
                    )
            else:
                print(f"\n\t{player.name} doubles down on hand!\n")
                player.double_down = True
                player.add_card(self._dealer.deal)
                player.wage(self._players[player]["wager1"])
                self._players[player]["wager1"] = (
                    self._players[player]["wager1"] * 2
                )

            self.new_hand(player)
            if player.score > 21 or player.score2 > 21:
                print(f"\t{player.name} Busts!\n")
