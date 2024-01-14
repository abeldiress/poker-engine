# Author: Kellen Sun
# Date: October 21st, 2023 - now
# Project Name: PokerV1
# Description:
# A library for Texas hold 'em to allow bots to interact with game rules
# Allows bot development to focus on strategy and algorithm implementation

import random

class System:
    """
    A class to return queries that players are asking for.
    """
    def __init__(self, playerlist):
        # pass in the playerlist as key identifiers
        self.cards = Cards(playerlist)
        self.cards.deal(playerlist)
        starting_amount = 1000
        self.playermoney = {}
        for player in playerlist:
            self.playermoney[player] = starting_amount

    def my_cards(self, p_key):
        return self.cards.player_cards[p_key]





class Cards:
    """
    A class to manage the position, existence and movement of cards
    around the table.
    """
    def __init__(self, playerlist):
        """Called at the start of new round."""
        self.deck = Cards.shuffle_deck()
        self.discard = [] 
        # list of cards that have been burned
        self.player_cards = {} # lists of players with the cards they have
        # playerlist is the most general variable here
        # It should contain a list of player objects
        for player in playerlist:
            self.player_cards[player.player_name] = [] # no cards yet
        self.table_cards = []

    def shuffle_deck(self):
        """Returns a list of a shuffled deck of 52 cards"""
        cards = []
        # first letter represents the value Ace through King
        # second letter represents the suit
        for i in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", 
                  "J", "Q", "K"]:
            for j in ["H", "S", "C", "D"]:
                cards.append(i+j)
        # end of list is top of deck
        return random.shuffle(cards)

    def deal(self, playerlist):
        """Deals the cards to the players"""
        for i in range(2):
            for player in self.player_cards.keys():
                self.player_cards[player].append(self.deck.pop())
        for player in playerlist:
            player.cards = self.player_cards[player]
            # Could later remove the .player_cards var and just use the
            # player object

    def burn(self):
        """Burns 1 card."""
        self.discard.append(self.deck.pop())

    def flop(self):
        """Deals the cards for the flop (first 3)"""
        self.burn()
        for i in range(3):
            self.table_cards.append(self.deck.pop())

    def turn(self):
        """Deals the cards for the turn (4th)"""
        self.burn()
        self.table_cards.append(self.deck.pop())

    def river(self):
        """Deals the cards for the river (5th)"""
        self.burn()
        self.table_cards.append(self.deck.pop())

class Player:
    """A collection of all information related to a player."""
    def __init__(self, name, cash) -> None:
        self.player_name = name #player's name a string
        self.cash = cash
        self.contributed = 0
        # amount that you put into the pot
        self.cards = []
        self.in_game = True
    
    def fold(self):
        self.in_game = False
    
    def check(self):
        pass

    def call(self):
        pass

    def bet(self, amount, min_bet):
        if amount <= self.cash and amount >= min_bet:
            self.cash -= amount
            self.contributed += amount
        elif amount >= min_bet:
            return "Insufficient cash supply"
        else:
            return "Bet amount too low"
    
    def big_blind(self, smallb):
        # smallb represents the small blind amount
        self.cash -= 2*smallb
        self.contributed += 2*smallb
    
    def small_blind(self, smallb):
        self.cash -= smallb
        self.contributed += smallb


class Money:
    """
    A class to manage the movement and counting of money.
    """
    def __init__(self):
        """Called at the start of new round."""
        self.pot = 0
        