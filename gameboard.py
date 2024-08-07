import tkinter as tk
from tkinter import messagebox
from cards import Cards
from datetime import datetime
import os

class GameBoard:
    def __init__(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.title("Blackjack Game")

        # Set background color, window size, and minimum size
        self.bgColor = "cornflower blue"
        self.mainWindow.configure(bg=self.bgColor)
        self.mainWindow.geometry("1100x800")
        self.mainWindow.minsize(1100, 800)

        # Load the icon
        self.mainWindow.iconbitmap('images/icon.ico')

        # Add BLACKJACK title
        self.titleLabel = tk.Label(self.mainWindow, text="BLACKJACK", fg="black", bg=self.bgColor, font=("Roboto", 24, "bold"))
        self.titleLabel.place(relx=0.5, rely=0.02, anchor='n')

        # Initialize player credits
        self.credits = 100
        self.creditsLabel = tk.Label(self.mainWindow, text=f"Credits: {self.credits}", fg="black", bg=self.bgColor, font=("Roboto", 16, "bold"))
        self.creditsLabel.place(relx=0.01, rely=0.01, anchor='nw')

        # Create sections for dealer and player
        self.createSections()

        # Add text box for credits input
        self.addCreditsInput()

        # Add buttons
        self.addButtons()

        # Load card images and create deck
        cardFolder = 'cards'  # Specify the path to the card images folder
        self.deck = Cards(cardFolder)
        self.playerHand = []
        self.dealerHand = []
        self.currentBet = 0

        # Ensure results directory exists
        resultsDir = 'results'
        if not os.path.exists(resultsDir):
            os.makedirs(resultsDir)

        # Create or clear the results file at the start of the session
        self.resultsFilePath = os.path.join(resultsDir, 'game_results.txt')
        with open(self.resultsFilePath, 'w') as file:
            file.write(f"Game Session Started - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    def createSections(self):
        # Create a section for the dealer's cards
        self.dealerFrame = tk.LabelFrame(self.mainWindow, text="Dealer", bg=self.bgColor, fg="black", font=("Roboto", 16, "bold"), padx=10, pady=10, bd=5, relief="solid")
        self.dealerFrame.place(relx=0.1, rely=0.09, relwidth=0.8, relheight=0.3)

        # Create a section for the player's cards
        self.playerFrame = tk.LabelFrame(self.mainWindow, text="Player", bg=self.bgColor, fg="black", font=("Roboto", 16, "bold"), padx=10, pady=10, bd=5, relief="solid")
        self.playerFrame.place(relx=0.1, rely=0.44, relwidth=0.8, relheight=0.3)

        # Add hand value label for player
        self.playerHandValueLabel = tk.Label(self.mainWindow, text="Player hand Value: 0", fg="black", bg=self.bgColor, font=("Roboto", 12))
        self.playerHandValueLabel.place(relx=0.1, rely=0.77, anchor='sw')

    def addCreditsInput(self):
        # Create input for player to enter bet credits
        creditsFrame = tk.Frame(self.mainWindow, bg=self.bgColor)
        creditsFrame.place(relx=0.5, rely=0.82, anchor='n')

        creditsLabel = tk.Label(creditsFrame, text="Enter credits to bet:", fg="black", bg=self.bgColor, font=("Roboto", 16, "bold"))
        creditsLabel.grid(row=0, column=0, padx=5)

        self.creditsEntry = tk.Entry(creditsFrame, width=5, font=("Roboto", 16))
        self.creditsEntry.grid(row=0, column=1, padx=5)

    def addButtons(self):
        # Create button section
        buttonFrame = tk.Frame(self.mainWindow, bg=self.bgColor)
        buttonFrame.place(relx=0.5, rely=0.88, anchor='n')

        buttonWidth = 10
        buttonHeight = 1

        buttonColor = "light grey"
        textColor = "black"

        # Create Bet 10 button
        self.bet10Button = tk.Button(buttonFrame, text="Bet 10", font=("Roboto", 12, "bold"), command=lambda: self.placeBet(10), width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.bet10Button.grid(row=0, column=0, padx=10, pady=(0, 10))

        # Create Bet 25 button
        self.bet25Button = tk.Button(buttonFrame, text="Bet 25", font=("Roboto", 12, "bold"), command=lambda: self.placeBet(25), width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.bet25Button.grid(row=0, column=2, padx=10, pady=(0, 10))

        # Create Hit button
        self.hitButton = tk.Button(buttonFrame, text="Hit", font=("Roboto", 12, "bold"), command=self.hit, state=tk.DISABLED, width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.hitButton.grid(row=1, column=0, padx=10)

        # Create Deal button
        self.dealButton = tk.Button(buttonFrame, text="Deal", font=("Roboto", 12, "bold"), command=self.deal, width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.dealButton.grid(row=1, column=1, padx=10)

        # Create Stand button
        self.standButton = tk.Button(buttonFrame, text="Stand", font=("Roboto", 12, "bold"), command=self.stand, state=tk.DISABLED, width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.standButton.grid(row=1, column=2, padx=10)

        self.hitOrStandLabel = tk.Label(self.mainWindow, text="", fg="black", bg=self.bgColor, font=("Roboto", 16, "bold"))
        self.hitOrStandLabel.place(relx=0.5, rely=0.78, anchor='n')

        # Create Quit button
        self.quitButton = tk.Button(self.mainWindow, text="Quit", font=("Roboto", 12, "bold"), command=self.quitGame, width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.quitButton.place(relx=0.98, rely=0.02, anchor='ne')

        # Create Game Rules button
        self.rulesButton = tk.Button(self.mainWindow, text="Game Rules", font=("Roboto", 12, "bold"), command=self.showGameRules, width=buttonWidth, height=buttonHeight, bg=buttonColor, fg=textColor)
        self.rulesButton.place(relx=0.98, rely=0.98, anchor='se')

        # Show game rules at the start
        self.showGameRules(initial=True)

    def placeBet(self, amount):
        # Set the bet amount in the credits entry and call deal
        self.creditsEntry.delete(0, tk.END)
        self.creditsEntry.insert(0, str(amount))
        self.deal()

    def deal(self):
        # Handle the initial deal of the game
        bet = self.creditsEntry.get()
        if not self.validateBet(bet):
            return

        self.currentBet = int(bet)
        self.credits -= self.currentBet
        self.creditsLabel.config(text=f"Credits: {self.credits}")

        # Clear previous hands
        self.playerHand = []
        self.dealerHand = []
        for widget in self.playerFrame.winfo_children():
            widget.destroy()
        for widget in self.dealerFrame.winfo_children():
            widget.destroy()

        # Deal two cards to player and dealer
        for i in range(2):
            self.playerHand.append(self.deck.dealCard())
            self.dealerHand.append(self.deck.dealCard())

        # Show player's cards
        self.showPlayerCards()

        # Show dealer's cards (one face down)
        self.showDealerCards(initial=True)

        # Update player's hand value
        self.updatePlayerHandValue()

        # Check for blackjack
        if self.checkBlackjack(self.playerHand):
            self.revealDealerCards()
            if self.checkBlackjack(self.dealerHand):
                self.showResult("Push!\nBoth you and the dealer have blackjack.", 0)
            else:
                self.showResult("You win!\nYou have a blackjack.", self.currentBet * 1.5)
        else:
            self.hitOrStandLabel.config(text="Would you like to Hit or Stand?")
            self.enableButtons()
            self.disableFastBetButtons()

    def checkBlackjack(self, hand):
        # Check if a hand is a blackjack
        return self.calculateHandValue(hand) == 21 and len(hand) == 2

    def revealDealerCards(self):
        # Show all dealer cards
        self.showDealerCards(initial=False)

    def showDealerCards(self, initial):
        # Display dealer's cards, with one face down if initial
        for widget in self.dealerFrame.winfo_children():
            widget.destroy()
        for i, (suit, rank, image) in enumerate(self.dealerHand):
            if initial and i == 1:
                cardLabel = tk.Label(self.dealerFrame, image=self.deck.cardImages['back'], bg=self.bgColor)
            else:
                cardLabel = tk.Label(self.dealerFrame, image=image, bg=self.bgColor)
            cardLabel.pack(side=tk.LEFT, padx=10, pady=(10, 0))

    def showResult(self, message, amount):
        # Show game result and update credits
        if amount > 0:
            message += f"\nYou won {amount} credits."
            self.credits += amount
        elif amount < 0:
            message += f"\nYou lost {abs(amount)} credits."
        else:
            message += "\nIt's a push."

        self.creditsLabel.config(text=f"Credits: {self.credits}")
        self.saveGameResult(message, amount)

        result = messagebox.askyesno("Game Result", f"{message}\n\nDo you want to continue playing?")
        if result:
            self.resetBoard()
        else:
            self.resetBoard()
            self.quitGame()

    def saveGameResult(self, message, amount):
        # Save the game result to a file
        with open(self.resultsFilePath, 'a') as file:
            file.write(f"Game Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Bet Amount: {self.currentBet}\n")
            file.write(f"{message}\n")
            file.write(f"Remaining Credits: {self.credits}\n\n")

    def updatePlayerHandValue(self):
        # Update the player's hand value display
        value = self.calculateHandValue(self.playerHand)
        self.playerHandValueLabel.config(text=f"Player hand Value: {value}")

    def calculateHandValue(self, hand):
        # Calculate the value of a hand
        value = 0
        aceCount = 0
        for suit, rank, image in hand:
            if rank in ['jack', 'queen', 'king']:
                value += 10
            elif rank == 'ace':
                aceCount += 1
                value += 11
            else:
                value += int(rank)
        
        while value > 21 and aceCount:
            value -= 10
            aceCount -= 1
        
        return value

    def validateBet(self, bet):
        # Validate the bet amount
        try:
            bet = int(bet)
            if bet in [10, 15, 20, 25] and bet <= self.credits:
                return True
            else:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Bet", "Please enter a valid bet amount (10, 15, 20, 25) within your available credits.")
            self.creditsEntry.delete(0, tk.END)
            return False

    def hit(self):
        # Handle hit action
        self.playerHand.append(self.deck.dealCard())
        self.showPlayerCards()
        self.updatePlayerHandValue()
        handValue = self.calculateHandValue(self.playerHand)
        if handValue == 21:
            self.hitOrStandLabel.config(text="")
            self.stand()
        elif handValue > 21:
            self.showResult("Bust! You lose.", -self.currentBet)
            self.disableButtons()
            self.creditsLabel.config(text=f"Credits: {self.credits}")

    def stand(self):
        # Handle stand action
        self.hitOrStandLabel.config(text="")
        self.dealerPlay()

    def showPlayerCards(self):
        # Display player's cards
        for widget in self.playerFrame.winfo_children():
            widget.destroy()
        for suit, rank, image in self.playerHand:
            cardLabel = tk.Label(self.playerFrame, image=image, bg=self.bgColor)
            cardLabel.pack(side=tk.LEFT, padx=10, pady=(10, 0))

    def dealerPlay(self):
        # Dealer plays until reaching at least 17
        self.revealDealerCards()
        while self.calculateHandValue(self.dealerHand) < 17:
            self.dealerHand.append(self.deck.dealCard())
        self.showDealerCards(initial=False)
        dealerHandValue = self.calculateHandValue(self.dealerHand)
        playerHandValue = self.calculateHandValue(self.playerHand)
        if dealerHandValue > 21 or playerHandValue > dealerHandValue:
            self.showResult(f"You win!\nYour hand value: {playerHandValue}.\nDealer's hand value: {dealerHandValue}.", self.currentBet * 2)
        elif dealerHandValue == playerHandValue:
            self.showResult(f"Push!\nYour hand value: {playerHandValue}.\nDealer's hand value: {dealerHandValue}.", self.currentBet)
        else:
            self.showResult(f"You lose!\nYour hand value: {playerHandValue}.\nDealer's hand value: {dealerHandValue}.", -self.currentBet)
        self.disableButtons()

    def enableButtons(self):
        # Enable hit and stand buttons
        self.hitButton.config(state=tk.NORMAL)
        self.standButton.config(state=tk.NORMAL)
        self.dealButton.config(state=tk.DISABLED)
        self.disableFastBetButtons()

    def disableButtons(self):
        # Disable hit and stand buttons
        self.hitButton.config(state=tk.DISABLED)
        self.standButton.config(state=tk.DISABLED)
        self.dealButton.config(state=tk.NORMAL)
        self.enableFastBetButtons()

    def disableFastBetButtons(self):
        # Disable quick bet buttons
        self.bet10Button.config(state=tk.DISABLED)
        self.bet25Button.config(state=tk.DISABLED)

    def enableFastBetButtons(self):
        # Enable quick bet buttons
        self.bet10Button.config(state=tk.NORMAL)
        self.bet25Button.config(state=tk.NORMAL)

    def resetBoard(self):
        # Reset the game board for a new game
        self.playerHand = []
        self.dealerHand = []
        self.deck.returnCards(self.playerHand + self.dealerHand)
        self.deck.shuffleDeck()
        for widget in self.playerFrame.winfo_children():
            widget.destroy()
        for widget in self.dealerFrame.winfo_children():
            widget.destroy()
        self.creditsEntry.delete(0, tk.END)
        self.playerHandValueLabel.config(text="Player hand Value: 0")
        self.hitOrStandLabel.config(text="")
        self.disableButtons()

    def quitGame(self):
        # Quit the game
        self.mainWindow.destroy()

    def showGameRules(self, initial=False):
        # Display game rules in a message box
        rules = (
        "Blackjack Game Rules:\n"
        "1. The goal is to get as close to 21 without going over.\n"
        "2. Face cards (Jack, Queen, King) are worth 10 points.\n"
        "3. Aces can be worth 1 or 11 points, whichever makes a better hand.\n"
        "4. If the player goes over 21, you bust and lose the round.\n"
        "5. The dealer must hit until their cards total 17.\n"
        "6. Blackjack pays 1.5x the bet if the player wins with a blackjack.\n"
        "7. If both the player and dealer have blackjack, it's a push (tie)."
        )
        
        if initial:
            self.mainWindow.after(500, lambda: messagebox.showinfo("Game Rules", rules, icon='info'))
        else:
            messagebox.showinfo("Game Rules", rules, icon='info')
