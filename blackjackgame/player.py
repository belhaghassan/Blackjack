#!/usr/bin/env python3
# Bilal El-haghassan
# CPSC 386-04
# 2022-02-28
# bilalelhaghassan@csu.fullerton.edu
# @belhaghassan
#
# Lab 03-00
#
# This is PigGame, a game of DICE and Chance
#

"""Player class for our Pig Game."""

import time
from blackjackgame import cards

class Player:
    """Player class for Pig Game"""

  


class Dealer:
    """Dealer player class"""

    # fix cut card min and max
    def __init__(self, n_decks = 1, cut_card_min = 51,\
        cut_card_max = 51):
        self._deck = cards.Deck(cut_card_min, cut_card_max )
        for _ in range(n_decks - 1):
            self._dec.merge(cards.Deck(cut_card_min, cut_card_max ))

    def deal(self, player):
        pass

    def check_shoe(self):
        """Check to see fi the dealer has reaced the cut\
            card, if so re-prepare the shoe."""
        pass

