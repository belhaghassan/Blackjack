

from time import sleep
from blackjackgame import cards

class BlackJackGame:
    def __init__(self):
        self._deck = cards.Deck(1,10)
        # player read in any data files
        # dealer
        self._game_is_not_over = True

    def run(self):

        while self._game_is_not_over:
            print("Top of the game loop")
            sleep(1)
            
            

