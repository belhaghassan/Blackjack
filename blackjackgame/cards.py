from collections import namedtuple
import math
import random

Card = namedtuple('Card', ['rank', 'suit'])

def stringify_card(c):
    return f"{c.rank} of {c.suit}"

Card.__str__ = stringify_card

class Deck:
    ranks = ['Ace'] + [str(x) for x in range(2, 11)]\
         + ['Jack', 'Queen', 'King']
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = list(range(1,11)) + [10, 10, 10]  
    values = dict(zip(ranks, values))

    def __init__(self, cut_card_position_min,\
        cut_card_position_max):
        self._cut_card_position = random.randrange(\
            cut_card_position_min,\
            cut_card_position_max)
        print('cut card is at ', self._cut_card_position)
        self._cards = [Card(rank, suit) \
            for suit in self.suits for rank in self.ranks]
    
    def needs_shuffle(self):
        return len(self._cards) <= self._cut_card_position

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)
    
    def __str__(self):
        return '\n'.join(map(str, self._cards))
    
    def merge(self, the_other_deck):
        self._cards = self._cards + the_other_deck._cards

    def cut(self):
        p = math.floor(len(self._cards) * .2)
        half = (len(self._cards) // 2 ) + \
        random.randrange(-p, p)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, n=1):
        return [self._cards.pop() for _ in range(n)]

    def shuffle(self, n=1):
        for _ in range(n):
            random.shuffle(self._cards)

def demo():
    # c = Card('9', 'Diamonds')
    # s = stringify_card(c)
    # print(c)
    d = Deck()
    for _ in range(3):
        d.merge(Deck())
    
    # d = Deck()
    # for index in range(len(d)):
    #     print(d[index], d.values[d[index].rank])
    return d

if __name__ == '__main__':
    d = Deck(24, 38)
    print(d)
    d.shuffle(10)
    d.cut()
    print('\nShuffled')
    print(d)
