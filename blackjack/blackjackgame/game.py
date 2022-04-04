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

import time
import pickle
import os
from blackjackgame import cards
from blackjackgame import player as Player

class BlackJackGame:
    def __init__(self):
        self._num_of_players = 0
        self._dealer = Player.Dealer("Dealer")
        self._players = {}
        self._ai_players = ["Optimus Prime", "Megatron", "Zora", "Skynet"]
        self._game_is_not_over = True
        self.line = (
        "\n\t"
        "******************************************************************"
        "\n"
        )

    def to_file(self, pickle_file, players):
        """Write the list players to the file pickle_file."""
        with open(pickle_file, 'wb') as file_handle:
            pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


    def from_file(self, pickle_file):
        """Read the contents of pickle_file, decode it, and return it as players."""
        with open(pickle_file, 'rb') as file_handle:
            players = pickle.load(file_handle)
        return players

    def new_hand(self, player):
        """Print out of current player and Dealers hand"""
        time.sleep(0.5)
        player.add_score()
        self._dealer.add_score()
        self.hand(self._dealer)
        time.sleep(1)
        print(
            f"\tCurrent Score: {self._dealer.score}\n"
        )

        self.hand(player)
        time.sleep(1)

    def card_template(self, rank, suit):
        """Card graphic template"""
        if rank == 10:
            return (
                "\t ___________\n"
                f'\t|{rank}{suit}        |\n'
                '\t|           |\n'
                '\t|           |\n'
                f'\t|     {suit}     |\n'
                '\t|           |\n'
                '\t|           |\n'
                f'\t|        {suit}{rank}|\n'
                '\t|___________|\n\n'
            )
        return (
            "\t __________\n"
            f'\t|{rank}{suit}        |\n'
            '\t|          |\n'
            '\t|          |\n'
            f'\t|    {suit}     |\n'
            '\t|          |\n'
            '\t|          |\n'
            f'\t|        {suit}{rank}|\n'
            '\t|__________|\n\n'
        )

    def hand(self, player):
        """Graphical representation of player hand"""

        suits = {'Clubs': '♣', 'Hearts': '♥', 'Spades': '♠','Diamonds': '♦'}
        rank = {'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A'}

        time.sleep(1)
        cards = []

        if player.is_split:
            print(f"\n\t{player.name}'s Hand:")
            for idx, hand in enumerate(player.cards()):
                print(f"\tHand {idx + 1}\n")
                for card in hand:
                    if card.rank in rank:
                        rnk = rank[card.rank]
                    else:
                        rnk = card.rank
                    suit = suits[card.suit]
                    cards.append(self.card_template(rnk,suit))
                card_list = list(range(len(cards)))
                lines = [cards[i].splitlines() for i in card_list]
                for lis in zip(*lines):
                    print(*lis, sep='')
                print(
                    f"\tCurrent Score: {player.score}\n"
                    f"\tCurrent Wager: $"
                    f"{self._players[player][f'wager{idx + 1}']}"
                )
                time.sleep(1)
                cards.clear()
                print(self.line)
        else:
            print(f"\n\t{player.name}'s Hand:")
            for card in player.cards():
                if card.rank in rank:
                    rnk = rank[card.rank]
                else:
                    rnk = card.rank
                suit = suits[card.suit]
                if player.name == 'Dealer' \
                    and player.cards()[1] == card \
                        and player.hidden:
                    template = (
                    "\t ___________\n"
                    '\t|           |\n'
                    '\t|     _     |\n'
                    '\t|   /   \\   |\n'
                    '\t|       /   |\n'
                    '\t|     |     |\n'
                    '\t|     .     |\n'
                    '\t|           |\n'
                    '\t|___________|\n\n'
                    )
                else:
                    template = self.card_template(rnk,suit) 
                cards.append(template)
            card_list = list(range(len(cards)))
            lines = [cards[i].splitlines() for i in card_list]
            for lis in zip(*lines):
                print(*lis, sep='')
            print(
                f"\tCurrent Score: {player.score}\n"
                f"\tCurrent Wager: $"
                f"{self._players[player][f'wager1']}"
            )
            print(self.line)

        time.sleep(1)

    def player_input(self, num_of_players):
        """Take in and save player names"""

        players_dict = self._players
        for plyr in range(num_of_players):
            # player_name = input(f"\n\tPlayer {plyr + 1}'s name: ")
            player_name = 'Bilsabob'
            players_dict[Player.Player(player_name)] = {}

        if num_of_players < 2:
            for _ in range(2 - num_of_players):
                ai_name = self._ai_players.pop(0)
                players_dict[Player.ComputerPlayer(ai_name)] = {}
                self._num_of_players += 1
                time.sleep(0.5)
                print(f"\n\tAI {list(players_dict)[-1].name} joined the game")

        time.sleep(1)
    def hit_or_stay(self, players, hand):
        while players.hit_or_stand():
            print(self.line)
            players.add_card(self._dealer.deal, hand)
            players.add_score
            self.new_hand(players)
            if players.score > 21:
                print(f"\t{players.name} busts "
                f"and loses ${self._players[players]['wager1']} wager.")
                break

    def check_winners(self, player, hand, wager):
        """Check if player beat dealer"""
        players_dict = self._players
        if hand < 22:
            if self._dealer.score == 21 and hand == 21:
                print("\n\tDraw - Non winnings or losses.\n")            
            elif self._dealer.score > 22 or hand > self._dealer.score:
                print(
                    "\t\t\t\t******WINNER******\n"
                    f"\t{player.name} wins ${players_dict[player][wager]} wager\n"
                    f"\tStarting Balance: {player.get_balance}"
                )
                player.win(players_dict[player][wager])
                print(
                    f"\tNew Balance with winnings:"
                    f" {player.get_balance}"
                    f"{self.line}\n"
                    )
            else:
                print(
                    f"\t{player.name} loses ${players_dict[player][wager]} wager\n"
                    f"\tStarting Balance: {player.get_balance}"
                    f"{self.line}\n"
                )
                player.lose(players_dict[player][wager])
                print(
                    f"\tNew Balance after losing: "
                    f"{player.get_balance}"
                    f"{self.line}\n"
                )
        else:
            print(f"\t{player.name} loses ${players_dict[player][wager]} wager\n")
            print(f"\tStarting Balance: {player.get_balance}\n")
            player.lose(players_dict[player][wager])
            print(f"\tNew Balance after losing: {player.get_balance}\n\n")
            print(self.line)

        if 'insurance' in players_dict[player] and self._dealer.score == 21:
            print(
                "\t\t\t\t******WINNER******\n"
                f"{player} wins insurance wager of {players_dict[player]['insurance']}"
            )


    def run(self):
        """Main BlackJack run function"""

        welcome = """
         ________________________________________________________________
        |                                                                |
        |    ♣  ♥  ♠  ♦                                    ♣  ♥  ♠  ♦    |
        |                           WELCOME                              |
        |                             TO                                 |
        |                                                                |
        |         ___   __            __       __            __          |
        |        / _ ) / /___ _ ____ / /__ __ / /___ _ ____ / /__        |
        |       / _  |/ // _ `// __//  '_// // // _ `// __//  '_/        |
        |      /____//_/ \\_,_/ \\__//_/\\_\\ \\___/ \\_,_/ \\__//_/\\_\\         |  
        |                                                                |
        |                                                                |
        |                         ____ ___________                       |
        |                        |    |           |                      |
        |                        | J♠ |A♠         |                      |
        |                        |    |           |                      |
        |                        |    |     ♠     |                      |
        |                        |    |           |                      |
        |                        |    |        A♠ |                      |
        |                        |____|___________|                      |
        |                                                                |
        |                                                                |
        |    ♣  ♥  ♠  ♦                                    ♣  ♥  ♠  ♦    |
        |________________________________________________________________|
        """
        print('\t\t', welcome)
        print(self.line)

        # Ask user how many players are going to play?
        while True:
            print("\tHow many players: [1 - 4]? \n\t" , end=" ")
            self._num_of_players = int(f"{input()}")
            if self._num_of_players <= 4 and self._num_of_players >= 1:
                break
            print("\tInvalid number of players. Try again.\n")

        self.player_input(self._num_of_players)
        print(self.line)

        dealer = self._dealer

        # self.to_file('players.pkl', players_dict)

        while self._game_is_not_over:
            if os.path.exists('players.pkl'):
                self._players = self.from_file('players.pkl')

            players_dict = self._players
            # Players asked to place bet
            for plyr in players_dict:
                players_dict[plyr] = {'wager1': plyr.place_bet()}

            # Deal to two cards to each player
            for _ in range(2):
                for plyr in players_dict:
                    if players_dict[plyr]['wager1'] > 0:
                        plyr.add_card(dealer.deal)
                dealer.add_card(dealer.deal)

            print(self.line)
            # Player's opportunity to split, double down or buy insurance
            for players in players_dict:
                self.new_hand(players)
                if cards.card_value(dealer.cards()[0]) == 10 or dealer.cards()[0].rank == "Ace":
                    insurance = input("\tWould you like to buy insurance? ('yes' or 'no') \n\t")
                    if insurance == ('y' or 'yes'):
                        players_dict[players]['insurance']\
                            = players.place_bet()

                # Check if player can split
                # if players.cards()[0].rank == players.cards()[1].rank and\
                if (players_dict[players]['wager1'] * 2) < players.get_balance:
                    split = input("\tWould you like to split? \n\t")
                    if split == ('y' or 'yes'):
                        players.split()
                        players.add_card(dealer.deal, 0)
                        players.add_card(dealer.deal, 1)
                        players_dict[players]['wager2'] = players_dict[players]['wager1']
                        self.new_hand(players)

                # Check if player wants to double down
                if players_dict[players]['wager1'] * 2 < players.get_balance:
                    self.double_down(players)

                if players.is_split:
                    if players.double_down and players.double_down2:
                        self.hit_or_stay(players, 0)
                        self.hit_or_stay(players, 1)
                    elif players.double_down:
                        self.hit_or_stay(players, 1)
                    elif players.double_down2:
                        self.hit_or_stay(players, 0)
                elif players.double_down is False:
                    self.hit_or_stay(players, 0)
            # Dealers move
            dealer.show
            dealer.add_score()
            print(self.line)
            self.hand(dealer)
            time.sleep(1)
            print(f"\tDealer's score: {dealer.score}")
            while dealer.hit_or_stand() and dealer.score < 22:
                print(self.line)
                dealer.add_card(dealer.deal)
                dealer.add_score()
                self.hand(dealer)
            if dealer.score > 21:
                print("\tDealer Busts!")

            # Check which players win
            for player in players_dict:
                print(self.line)
                self.new_hand(player)
                print(self.line)
                if players.score2:
                    self.check_winners(player, player.score, 'wager1')
                    self.check_winners(player, player.score2, 'wager2')
                else:
                    self.check_winners(player, player.score, 'wager1')
                player.reset
            dealer.reset
            dealer.hide

            self.to_file('players.pkl', players_dict)

            print(self.line)

            if input(
                f"\n\tPlayer {list(players_dict)[0].name} would you like to "
                "play again? \n\t['y' or 'yes' or 'n' or 'no']\n\t"
            ) == ('y' or'yes'):
                print("\n\tAnother one!\n")
            else:
                self._game_is_not_over = False
                print("\n\tGameOver")

    def double_down(self, players):
        """Function to double down on a players wager"""
        players_dict = self._players

        double_down = input("\tWould you like to double down? ('yes' or 'no')\n\t")
        if double_down == ('y' or 'yes'):
            if players.is_split:
                if players_dict[players]['wager1'] * 4 < players.get_balance:
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
                if choice == 'both' and players_dict[players]['wager1'] * 4 < players.get_balance:
                    print(f"\n\t{players} will double down on both hands!\n")
                    players.add_card(self._dealer.deal)
                    players.add_card(self._dealer.deal, 1)
                    players.double_down = True
                    players.double_down2 = True
                    players_dict[players]['wager1'] = players_dict[players]['wager1'] * 2
                    players_dict[players]['wager2'] = players_dict[players]['wager1']
                elif choice == "2":
                    print(f"\n\t{players} will double down on 2nd hand!\n")
                    players.add_card(self._dealer.deal, 1)
                    players.double_down2 = True 
                    players_dict[players]['wager2']\
                        = players_dict[players]['wager1'] * 2
                else:
                    print(f"\n\t{players} will double down on 1st hand!\n")
                    players.add_card(self._dealer.deal)
                    players.double_down = True
                    players_dict[players]['wager1']\
                        = players_dict[players]['wager1'] * 2
            else:
                players.double_down = True
                players_dict[players]['wager1']\
                    = players_dict[players]['wager1'] * 2

        
            if players.is_split and players.double_down is False or players.double_down2 is False:
                hand = 0 if players.double_down else 1
                if players.double_down2:
                    while players.hit_or_stand():
                        print(self.line)
                        players.add_card(self._dealer.deal, hand)
                        self.new_hand(players)
                        if players.score > 21:
                            print(f"\t{players.name} busts and loses"
                            f" ${players_dict[players][f'wager{hand + 1}']}"
                            " wager.")
                            time.sleep(1)
