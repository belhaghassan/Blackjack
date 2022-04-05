#!/usr/bin/env python3
# Bilal El-haghassan
# CPSC 386-04
# 2022-04-04
# bilalelhaghassan@csu.fullerton.edu
# @belhaghassan
#
# Lab 03-04
#
# This is BlackJackGame, a game of Cards and money
#

"""This is a game of BlackJackGame with 1 - 4 players"""

import time
import random
import pickle
from blackjackgame import cards


class Player:
    """Human player class"""

    def __init__(self, name, identifier):
        """Initialize a human player"""
        self._name = name
        self._identifier = identifier
        self._cards = []
        self._score = 0
        self._score2 = 0
        self._double_down = False
        self._double_down2 = False
        self._balance = 10000
        self._split = False

    @property
    def reset(self):
        """Resest players properties except balance"""
        self._cards.clear()
        self._score = 0
        self._score2 = 0
        self._double_down = False
        self._double_down2 = False
        self._split = False

    @property
    def name(self):
        """Return the player's name"""
        return self._name

    @property
    def identifier(self):
        """Return the player's id"""
        return self._identifier

    @property
    def score(self):
        """Return the player's score."""
        return self._score

    @property
    def score2(self):
        """Return the player's 2nd hand score."""
        return self._score2

    @property
    def get_balance(self):
        """Retrieve players balance"""
        return self._balance

    @property
    def is_split(self):
        """Returns split property"""
        return self._split

    @property
    def double_down(self):
        """Return true or false for first hand double down"""
        return self._double_down

    @property
    def double_down2(self):
        """Return true or false for 2nd hand double down"""
        return self._double_down2

    @double_down.setter
    def double_down(self, true_or_false):
        """Set true or false for first hand double down"""
        self._double_down = true_or_false

    @double_down2.setter
    def double_down2(self, true_or_false):
        """Set true or false for 2nd hand double down"""
        self._double_down2 = true_or_false

    def wage(self, wager):
        """Deduct wage from balance"""
        self._balance = self._balance - wager

    def add_balance(self, winnings):
        """Add wages plus winnings back to balance"""
        self._balance = self._balance + winnings

    def win(self, wager):
        """Add to balance"""
        self._balance += wager

    def lose(self, wager):
        """Deduct from balance"""
        self._balance -= wager

    def add_card(self, card, hand=0):
        """Add card to players hand"""
        if self.is_split:
            self._cards[hand].append(card)
        else:
            self._cards.append(card)

    def check_ace(self, hand, score):
        """Check and change value of Ace"""
        for card in hand:
            if score == "score0":
                if card.rank == "Ace" and self._score > 21:
                    self._score = self._score - 10
            else:
                if card.rank == "Ace" and self._score2 > 21:
                    self._score2 = self._score2 - 10

    def add_score(self):
        """Add up the player's score."""
        if self.is_split is False:
            score = 0
            for card in self.cards():
                if card.rank == "Ace":
                    score += 11
                else:
                    score += cards.card_value(card)
            self._score = score
            self.check_ace(self.cards(), "score0")
        else:
            score0 = 0
            score2 = 0
            for card in self.cards()[0]:
                if card.rank == "Ace":
                    score0 += 11
                else:
                    score0 += cards.card_value(card)
            for card in self.cards()[1]:
                if card.rank == "Ace":
                    score2 += 11
                else:
                    score2 += cards.card_value(card)
            self._score = score0
            self._score2 = score2
            self.check_ace(self.cards()[1], "score2")
            self.check_ace(self.cards()[0], "score0")

    def top_up(self):
        """Replenish funds from anonymous donor"""
        if self.get_balance < 1:
            self._balance = 10000
        print(
            f"\t{self.name}, you have been gifted $10000 from an Anonymous"
            " donor!"
        )

    def place_bet(self):
        """Place a players wager"""
        wage = int(input(f"\tPlayer {self.name}. How much do you wager? "))
        tries = 3
        while (wage > self.get_balance or wage < 0) and tries > 0:
            print(
                "\tInvalid wager entered, try again.\n",
                f"\tCurrent balance: ${self.get_balance}"
            )

            wage = int(input(f"\t{self.name}. How much do you wager? "))
            tries -= 1
        return wage if tries > 0 else 0

    def cards(self):
        """Returns players current cards"""
        return self._cards

    def split(self):
        """Splits a players hand into two hands"""
        self._cards = [[self._cards[0]], [self._cards[1]]]
        self._score = 0
        self._split = True

    def hit_or_stand(self):
        """Hit or stand methed"""
        time.sleep(0.5)
        print(
            f"\n\tWould {self.name} like to Hit or stand? \n"
            "\t(Type 'hit' or 'h' to hit, or just",
            "ENTER anykey to stand)\n\t",
        )
        time.sleep(0.5)
        decision = input("\t")

        if decision in ("h", "hit"):
            print(f"\n\t{self.name} will hit \n")
            return True
        print(f"\n\t{self.name} will stand \n")
        return False

    def __str__(self):
        """Convert the Player to a printable string."""
        return (
            f"\n\tHi, my name is {self._name} ({self.identifier})\n"
            f"\tBalance of {self.get_balance}\n"
        )

    def __repr__(self):
        """Python representation."""
        return (
            f"\n\tPlayer:"
            f"\t  Name    = {self.name}\n"
            f"\t  UserID  = {self.identifier}\n"
            f"\t  Score   = {self.score}\n"
            f"\t  Balance = {self.get_balance}"
        )


class ComputerPlayer(Player):
    """AI player class"""

    def __init__(self, name, identifier):
        """Initialize an AI player"""
        super().__init__(name, identifier)

    def place_bet(self):
        """AI random bet"""
        wage = 400
        print(f"\n\tPlayer {self.name}. How much do you wager? {wage}\n")
        time.sleep(0.5)
        return wage

    def hit_or_stand(self):
        """Hit or stay methed"""
        print(f"\n\tWould {self.name} like to Hit or stand? \n")
        time.sleep(0.5)
        print(
            "\t(Type 'hit'/'h' to hit, or anykey to stand)\n\t"
        )
        if self.score < 17:
            print(f"\t{self.name} hit\n")
            return True
        print(f"\t{self.name} will stay\n\t")
        return False


class Dealer(Player):
    """Dealer class"""

    def __init__(self, name, n_decks=8, min_cut=60, max_cut=80):
        """Initialize an AI dealer"""
        super().__init__(name, identifier=random.randint(100, 1000))
        self._hide_second = True
        self._balance = 10000000000000000000
        self._deck = cards.Deck()
        self._shoe = None
        self._cut_card_position = self.create_playing_deck(
            n_decks, min_cut, max_cut
        )

    @property
    def score(self):
        """Return the player's score."""
        return "?" if self.hidden else self._score

    @property
    def hidden(self):
        """Check to see if dealer should reveal second card dealt"""
        return self._hide_second

    @property
    def hide(self):
        """Hide second card dealt"""
        self._hide_second = True

    @property
    def show(self):
        """Reveal dealers second card"""
        self._hide_second = False

    @property
    def deal(self):
        """Distribute a card from the deck"""
        self.check_shoe()
        return self._shoe.pop()

    def create_playing_deck(self, n_decks, min_cut, max_cut):
        """Create and add shuffled decks to shoe with cut card"""
        cut_card_position = random.randrange(min_cut, max_cut)
        for _ in range(n_decks):
            self._deck.merge(cards.Deck())
        self._deck.shuffle(3)
        self._deck.cut()
        self._shoe = self._deck.cards
        return cut_card_position

    def check_shoe(self):
        """Check to see if the dealer has reaced the cut\
            card, if so re-prepare the shoe."""
        if len(self._deck) <= self._cut_card_position:
            print("\tCut card reached. Reshuffling...")
            time.sleep(1)
            self.create_playing_deck(8, 60, 80)
            print("\tReshuffing Complete.")

    def hit_or_stand(self):
        """Hit or stand  methed"""
        if self.score < 17:
            print(f"\t{self.name} hits\n")
            return True
        if self.score < 22:
            print(f"\t{self.name} will stand \n")
        return False

    def __str__(self):
        """Convert the Player to a printable string."""
        return (
            f"\tHi, I am the DEALER. Current score: "
            f"{'?' if self.hidden else self._score}"
        )

    def __repr__(self):
        """Python representation."""
        return (
            f"\tPlayer(name={self._name}, score="
            f"{'?' if self.hidden else self._score}"
            f"): Balance -> {self.get_balance}"
        )

def to_file(pickle_file, players):
    """Write the list players to the file pickle_file."""
    with open(pickle_file, 'wb') as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """Read the contents of pickle_file, decode it, and return it as players."""
    with open(pickle_file, 'rb') as file_handle:
        players = pickle.load(file_handle)
    return players
