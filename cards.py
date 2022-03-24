from collections import namedtuple
import random

Card = namedtuple('Card', ['rank', 'suit'])
def pretty_print_card(c):
    return f"{c.rank} of {c.suit}"

Card.__str__ = pretty_print_card

class Deck:
    ranks = ['Ace'] + list(map(str, list(range(2,11)))) + \
    'Jack Queen King'.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()    
    values = list(range(1,11)) + [10, 10, 10]  
    value_dict = dict(zip(ranks, values))
 
    def __init__ (self):
        self._cards = [Card(rank, suit)\
            for rank in Deck.ranks for suit in Deck.suits]  

    def shuffle(self):
        shuffle(self._cards)

    def __str__(self):
        return "\n".join([f"{i}, {j}" for i, j in enumerate(self._cards)])

if __name__ == '__main__':
    c = Card('Queen', 'Spade')
    # print(c)
    # print(str(c))

    # ranks = list(map(str, list(range(2,11))))


    # print(ranks)
    # print(suits)
    # print(ranks, len(ranks))
    # print(values, len(values))

    # print(value_dict)
    # print(value_dict['10'])

    # cards = [Card(ranks, suits) for rank in ranks for suit in suits]
    # for card in value_dict:
    #     print(card)