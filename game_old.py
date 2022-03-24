#!/usr/bin/env python3
# Bilal El-haghassan
# CPSC 386-04
# 2022-02-28
# bilalelhaghassan@csu.fullerton.edu
# @belhaghassan
#
# Lab 02-00
#
# This is PigGame, a game of DICE and Chance
#

"""Game class for our Pig Game."""

import random
import time
from pig_game import die
from pig_game import player


class PigGame:
    """PigGame class"""

    def __init__(self):
        self._players = []
        self._turn_score = 0
        self._num_of_players = 0
        self._die = die.Die()

        welcome = """
        ***************************************************************\n
                            WELCOME TO PIG GAME!
                                A GAME OF DICE

                    **********************************
                    *             _______            *
                    *           /\\       \\           *
                    *          /()\\   ()  \\          *
                    *         /    \\_______\\         *
                    *         \\    /()     /         *
                    *          \\()/   ()  /          *
                    *           \\/_____()/           *
                    *                                *
                    *       Art by Joan G. Stark     *
                    **********************************

                 PACKED WITH RISK, FUN, AND A LITTLE BIT OF LUCK
                        PLAY WITH UP TO 4 PLAYERS!\n
        ***************************************************************\n
        """
        print(welcome)

    def opponent_score(self, opponent):
        """Opponent score getter"""
        for plyr in self._players:
            if opponent == plyr:
                continue
            return plyr.score

    @property
    def die(self):
        """Return Pig game die instance"""
        return self._die

    @property
    def turn_score(self):
        """Current turn score property"""
        return self._turn_score

    @turn_score.setter
    def turn_score(self, new_turn_score):
        self._turn_score = new_turn_score

    def game_state(self):
        """Game state method"""
        print(
            "\n\t",
            "***************************************************************",
            "\n\t\t\t\tGAME STATE",
        )
        time.sleep(0.5)
        for plyr in self._players:
            print(f"\n\t\t\tPlayer {plyr.name} has a score of {plyr.score}.")
        time.sleep(0.5)
        print(
            "\n\t",
            "***************************************************************",
        )

    def player_input(self, num_of_players):
        """Take in and save player names"""

        for plyr in range(num_of_players):
            self.die.roll_die()
            player_name = input(f"\n\tEnter Player {plyr + 1}'s name: ")
            self._players.append(player.Player(player_name, self.die.roll))

        if num_of_players < 2:
            num_of_players = 2
            self.die.roll_die()
            ai_players = ["Optimus Prime", "Megatron", "Zora", "Skynet"]
            bot = random.choice(ai_players)
            self._players.append(
                player.ComputerPlayer(self.die.roll, bot, self)
            )
            print(
                f"\n\t{self._players[0].name}, you will be playing against ",
                f"AI {self._players[1].name}!\n\n\n",
                "\n",
            )

        self._num_of_players = num_of_players
        print(
            "       *\t*\t*\t*\t*\t*\t*\t*\t   *\n",
            "\n\t\t\tWelcome Players: \n\n",
            end="",
        )
        for plyr in self._players:
            print(f"\t{plyr.name.upper()}")
            if plyr != self._players[self._num_of_players - 1]:
                print("\t  &")
        print(
            f"\n\tThis will be a {num_of_players} player game\n",
            "\n\tFirst player to 30 or more points wins!\n",
        )
        time.sleep(1)

    def run(self):
        """Main piggame run function"""

        # Ask user how many players are going to play?
        while True:
            print("\tHow many players would like to play? [1 - 4]", end=" ")
            self._num_of_players = int(f"{input()}")
            if self._num_of_players <= 4 and self._num_of_players >= 1:
                break
            print("\tInvalid number of players. Try again.\n")

        # Take and save player names
        self.player_input(self._num_of_players)

        # Sort players in list by order of die roll (highest goes first)
        self._players.sort(key=lambda p: p.order, reverse=True)

        # Current player in list to roll the dice.
        current_player_index = 0

        # Top score to end game when a player's score surpasses 30
        top_score = 0
        current_player = self._players[current_player_index]

        print(f"\t\t\t {current_player.name.upper()} WILL GO FIRST!")
        time.sleep(1)
        while top_score < 30:

            # Current players score for their turn
            self.turn_score = 0
            roll_number = 1
            print(f"\t\t\t  ****{current_player.name.upper()}'S TURN****\n")

            time.sleep(1)

            self.die.roll_die()
            roll = self.die.roll

            print(f"\t{current_player}'s roll # {roll_number}: {roll}")
            if roll == 1:
                time.sleep(1)
                print(f"\t{current_player} loses turn!\n")

            else:
                self.turn_score += roll
                print(
                    f"\tIf {current_player} holds they will have ",
                    current_player.score + self.turn_score,
                    "\n",
                )

            # Checks to see if player wants to roll or hold
            if self.turn_score != 1 and self.turn_score != 0:
                while current_player.roll_or_hold():
                    time.sleep(0.5)
                    self.die.roll_die()
                    next_roll = self.die.roll
                    roll_number += 1
                    print(
                        f"\n\t{current_player}'s roll #",
                        f"{roll_number}: {next_roll}",
                    )
                    time.sleep(0.5)
                    if next_roll == 1:
                        print(f"\t{current_player} loses turn!")
                        self.turn_score = 0
                        break
                    self.turn_score += next_roll
                    print(
                        f"\tIf {current_player} holds they will have ",
                        current_player.score + self.turn_score,
                        "\n",
                    )
                    time.sleep(1)

            if self.turn_score != 1 and self.turn_score != 0:
                current_player.score = current_player.score + self.turn_score

            if current_player.score > top_score:
                top_score = current_player.score

            next_player_index = current_player_index + 1
            current_player_index = next_player_index % self._num_of_players
            current_player = self._players[current_player_index]
            self.turn_score = 0
            roll_number = 1
            self.game_state()

        winner_index = (current_player_index - 1) % self._num_of_players
        current_player = self._players[winner_index]
        print(
            "\n\n\n\n\n\n\t",
            "***************************************************************",
            f"\n\n\n\n\t\t\t\t****{current_player.name.upper()} Wins!****\n",
            "\n\n\n\t",
            "***************************************************************",
            "\n\n\n",
        )
