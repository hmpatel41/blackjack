import tkinter as tk
import os
import random

class Cards:
    def __init__(self, cardFolder):
        # Initialize the card folder and create empty lists for cards and used cards
        self.cardFolder = cardFolder
        self.cards = []
        self.usedCards = []
        self.cardImages = self.loadCardImages()
        self.buildDeck()

    def loadCardImages(self):
        # Load card images from the specified folder
        cardImages = {}
        for filename in os.listdir(self.cardFolder):
            if filename.endswith('.png'):
                cardName = filename.split('.')[0]
                cardPath = os.path.join(self.cardFolder, filename)
                cardImage = tk.PhotoImage(file=cardPath).subsample(6, 6)
                cardImages[cardName] = cardImage
        return cardImages

    def buildDeck(self):
        # Build the deck of cards by combining suits and ranks
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                cardName = f"{rank}_of_{suit}"
                cardImage = self.cardImages[cardName]
                self.cards.append((suit, rank, cardImage))
        self.shuffleDeck()

    def shuffleDeck(self):
        # Shuffle the deck of cards
        random.shuffle(self.cards)

    def dealCard(self):
        # Deal a card from the deck, reshuffling used cards if the deck is empty
        if not self.cards:
            self.cards, self.usedCards = self.usedCards, []
            self.shuffleDeck()
        card = self.cards.pop()
        self.usedCards.append(card)
        return card

    def returnCards(self, cards):
        # Return a list of cards to the used cards pile
        self.usedCards.extend(cards)
