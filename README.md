This document provides an overview of the Blackjack game implementation using Python's Tkinter library. The game simulates a simple Blackjack game using standard rules mentioned later in this document.

How to play the game:
1.	Starting the Game: Launch the game by running main.py. The game window will open, displaying the Blackjack title, your current credits, and sections for dealer and player cards.
2.	Placing a Bet:
•	Enter the amount you want to bet in the input field labeled "Enter credits to bet.
•	Alternatively, use the quick bet buttons ("Bet 10" and "Bet 25") to quickly set a bet amount.
•	Click the "Deal" button to place your bet and start the game.
3.	Dealing Cards:
•	After placing a bet, two cards will be dealt to both the player and the dealer.
•	One of the dealer's cards will be faced down.
4.	Player's Turn:
•	You can choose to "Hit" (draw another card) or "Stand" (keep your current hand).
•	The goal is to get as close to 21 points without going over.
•	If your hand value exceeds 21, you bust and lose the round.
5.	Dealer's Turn:
•	Once you stand, the dealer will reveal their face-down card and draw additional cards until their hand value reaches at least 17.
•	The dealer must follow strict rules for drawing cards and cannot make decisions like the player.
6.	Determining the Winner:
•	If your hand value is closer to 21 than the dealer's without exceeding 21, you win the round and earn credits based on your bet.
•	If the dealer's hand value is closer to 21, you lose the round and lose your bet.
•	If both hands have the same value, it’s a push (tie), and your bet is returned.
7.	Continuing the Game:
•	After the result is displayed, you can choose to continue playing by placing a new bet or quit the game.
8.	Viewing Game Rules:
•	Click the "Game Rules" button to view the rules of Blackjack at any time during the game.

References:
Source for cards images: https://code.google.com/archive/p/vector-playing-cards/downloads

