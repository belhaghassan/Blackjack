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

# redefine Card's __str__ to _str_card()
Card.__str__ = _str_card


class Deck:
    """Deck class to hold 52 French suited playing cards."""

    ranks = ['Ace'] + [str(x) for x in range(2, 11)]\
         + 'Jack Queen King'.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self):
        self._cards = [Card(rank, suit) \
            for suit in self.suits for rank in self.ranks]
    
    @property
    def cards(self):
        return self._cards

    def needs_shuffle(self):
        return len(self._cards) <= self._cut_card_position

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)
    
    def __str__(self):
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
        """Cut the deck at approximately the half way point +/- 20% of the cards."""
        extra = ceil(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + \
            randrange(-extra, extra)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, n_cards=1):
        """Deal n cards. Default is 1 card."""
        return [self._cards.pop(0) for x in range(n_cards)]

    def shuffle(self, n=1):
        for _ in range(n):
            shuffle(self._cards)

def card_value(card):
    """Return the numerical value of the rank of a given card."""
    return Deck.value_dict[card.rank]

# def demo():
#     # c = Card('9', 'Diamonds')
#     # s = stringify_card(c)
#     # print(c)
#     d = Deck()
#     for _ in range(3):
#         d.merge(Deck())
    
#     # d = Deck()
#     # for index in range(len(d)):
#     #     print(d[index], d.values[d[index].rank])
#     return d

# if __name__ == '__main__':
#     d = Deck(24, 38)
#     print(d)
#     d.shuffle()
#     card = d.deal()
#     print(card, d.values_dict[card[0][0]])

    # d.cut()
    # # print('\nShuffled')
    # print(d)
