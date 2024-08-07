import tkinter as tk
from gameboard import GameBoard

if __name__ == "__main__":
    # Initialize the main window
    mainWindow = tk.Tk()

    # Create an instance of the GameBoard class
    game = GameBoard(mainWindow)

    # Run the main loop
    mainWindow.mainloop()
