#!/usr/bin/env python3
# Bilal El-haghassan
# CPSC 386-04
# 2022-04-04
# bilalelhaghassan@csu.fullerton.edu
# @belhaghassan
#
# Lab 03-02
#
# This is BlackJackGame, a game of Cards and money
#

"""A French suited playing card class and a Deck of 52 cards class"""

from collections import namedtuple
from random import shuffle, randrange
from math import ceil

Card = namedtuple('Card', ['rank', 'suit'])


def _str_card(card):
    """Convert a card to a nicely formatted string"""
    return f'{card.rank} of {card.suit}'


Card.__str__ = _str_card


class Deck:
    """Deck class to hold 52 French suited playing cards."""
    string = 'Jack Queen King'
    ranks = ['Ace'] + [str(x) for x in range(2, 11)] + string.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self):
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    @property
    def cards(self):
        """Returns cards list"""
        return self._cards

    def __len__(self):
        """Returns length of deck"""
        return len(self._cards)

    def __str__(self):
        """Returns nice string format of cards"""
        return '\n'.join(map(str, self._cards))

    def merge(self, other_deck):
        """Merge the current deck with the deck passed as a parameter."""
        # Yes, we are accessing a protected member _cards of a client class.
        # We're breaking the rules. The alternative is to add an option to
        # remove the cards from the other_deck and via a method (i.e. deal())
        # and then add the cards to self._cards.
        # self._cards = self._cards + other_deck._cards
        self._cards = self._cards + other_deck.deal(len(other_deck))

    def cut(self):
        """Cut the deck at approximately the half way point +/- 20% of the
        cards."""
        extra = ceil(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-extra, extra)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, n_cards=1):
        """Deal n cards. Default is 1 card."""
        return [self._cards.pop(0) for x in range(n_cards)]

    def shuffle(self, num=1):
        """Shuffle the deck of cards"""
        for _ in range(num):
            shuffle(self._cards)


def card_value(card):
    """Return the numerical value of the rank of a given card."""
    return Deck.value_dict[card.rank]

def card_template(rank, suit):
    """Card graphic template"""
    if rank == "10":
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
