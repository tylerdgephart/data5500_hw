#Create a class for each individual card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11  # or 1, handled later
        else:
            return int(self.rank)

import random

#Create a class of a 52 card deck
class DeckOfCards:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.deck = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
    
    def shuffle_deck(self):
        random.shuffle(self.deck)

    def get_card(self):
        return self.deck.pop(0)

    def __repr__(self):
        return ', '.join([str(card) for card in self.deck])