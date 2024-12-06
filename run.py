import random

# Create a game board
def create_board(size=5):
    return [["~" for _ in range(size)] for _ in range(size)]

# Print the game board with row and column numbers (no borders)
def print_board(board, show_ships=False, label=""):
    print(f"\n{label}")
    print("   " + " ".join(str(i) for i in range(len(board[0]))))  # Column numbers aligned properly
    for idx, row in enumerate(board):
        if show_ships:
            # Show all board content, including ships
            print(f"{idx:2} " + " ".join(row))
        else:
            # Hide ships on the board and only show the results of guesses ('H' and 'X')
            print(f"{idx:2} " + " ".join('~' if cell == 'S' else cell for cell in row))

# Place multiple ships randomly on the board (without overlapping)
def place_multiple_ships(board, ship_count=3):
    ships = []
    while len(ships) < ship_count:
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        if (row, col) not in ships:  # Avoid duplicate positions
            ships.append((row, col))
            board[row][col] = "S"  # Mark ship position
    return ships

# Get player's guess with input examples (modified to loop if already guessed)
def get_player_guess(board_size, previous_guesses):
    while True:
        try:
            print(f"Enter a row (0 to {board_size - 1}) and column (0 to {board_size - 1}).")
            row = int(input("Guess Row: "))
            col = int(input("Guess Column: "))
            if 0 <= row < board_size and 0 <= col < board_size:
                if (row, col) in previous_guesses:
                    print("You have already guessed there! Try again.")
                else:
                    return row, col
            else:
                print("Invalid input! Row and column must be within the range 0 to", 
                      board_size - 1)
        except ValueError:
            print("Invalid input! Please enter integers only.")

# Computer's guess (random choice)
def get_computer_guess(board_size, previous_guesses):
    while True:
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        if (row, col) not in previous_guesses:
            return row, col

# Check if the guess is correct or already guessed (modified to reflect the change)
def check_guess(board, guess, ships, score, previous_guesses, is_player_turn=True):
    row, col = guess

    # If the guess is already made, return False to indicate invalid input
    if guess in previous_guesses:
        return False  # Don't use up a turn

    if guess in ships:
        print("Hit!")
        ships.remove(guess)  # Remove the hit ship
        board[row][col] = "H"  # Mark hit
        score['hits'] += 1
        previous_guesses.add(guess)  # Add the guess to the set of previous guesses
        if not ships:
            return True  # All ships are sunk
    elif board[row][col] in {"X", "H"}:
        print("You already guessed that!")
    else:
        print("Miss!")
        board[row][col] = "X"  # Mark miss
        score['misses'] += 1
        previous_guesses.add(guess)  # Add the guess to the set of previous guesses
    
    return False

# Play the game
def play_battleship(player_name):
    board_size = 5  # Change this to create larger boards
    ship_count = 3  # Number of ships to place
    turns = 10  # Number of guesses allowed

    # Player's board and ships (random placement for player)
    player_board = create_board(board_size)
    player_ships = place_multiple_ships(player_board, ship_count)
    player_score = {'hits': 0, 'misses': 0}  # Track hits and misses
    player_previous_guesses = set()  # Store previously guessed locations

    # Computer's board and ships
    computer_board = create_board(board_size)
    computer_ships = place_multiple_ships(computer_board, ship_count)
    computer_score = {'hits': 0, 'misses': 0}  # Track hits and misses
    computer_previous_guesses = set()  # Store previously guessed locations

    print(f"\nWelcome to Battleship, {player_name}!")
    print(f"The board is {board_size}x{board_size}. There are {ship_count} "
          f"battleships to sink.\n")
    print_board(player_board, show_ships=True, label="Your Board")  # Show ships' locations on the player's board
    print_board(computer_board, show_ships=False, label="Computer's Board")  # Do not show the computer's ships

    for turn in range(turns):
        # Player's turn
        print(f"\nTurn {turn + 1}/{turns} - Your Turn")
        guess = get_player_guess(board_size, player_previous_guesses)
        if check_guess(computer_board, guess, computer_ships, player_score, 
                       player_previous_guesses, is_player_turn=True):
            print("Congratulations, you sunk all the computer's ships!")
            break
        print_board(player_board, show_ships=True, label="Your Board")  # Always show player's ships
        print_board(computer_board, show_ships=False, label="Computer's Board")  # Hide computer ships

        # Computer's turn
        print(f"\nTurn {turn + 1}/{turns} - Computer's Turn")
        computer_guess = get_computer_guess(board_size, computer_previous_guesses)
        print(f"Computer guesses: {computer_guess[0]} {computer_guess[1]}")
        if check_guess(player_board, computer_guess, player_ships, computer_score, 
                       computer_previous_guesses, is_player_turn=False):
            print("The computer sunk your ships!")
            break
        print_board(player_board, show_ships=True, label="Your Board")  # Always show player's ships
        print_board(computer_board, show_ships=False, label="Computer's Board")  # Hide computer ships

    # Game over - Reveal the computer's ships
    print("\nGame Over!")
    print_board(player_board, show_ships=True, label="Your Board")  # Show player's board
    print_board(computer_board, show_ships=True, label="Computer's Board")  # Show computer's ships

    if not computer_ships and not player_ships:
        print("It's a tie! Both you and the computer sunk each other's ships!")
    elif not computer_ships:
        print("You won! You sunk all the computer's ships!")
    elif not player_ships:
        print("You lost! The computer sunk all your ships.")
    
    print(f"Final Score: {player_name} - {player_score['hits']} hits, "
          f"{player_score['misses']} misses.")
    print(f"Computer - {computer_score['hits']} hits, {computer_score['misses']} misses.")
    return player_score['hits']  # Return score to determine replay option

# Display how to play the game
def how_to_play():
    print("\nHow to Play Battleship:")
    print("1. The game board is a grid, represented by '~'.")
    print("2. You and the computer each have a set of ships placed at random locations "
          "on the board.")
    print("3. The ships on your board will be shown as 'S' for ships, but only for your view.")
    print("4. Each turn, you will guess a row and column (e.g., 2 3) to try and hit the "
          "computer's ships.")
    print("5. If you hit a battleship, it will be marked as 'H'.")
    print("6. If you miss, the grid will mark it with an 'X'.")
    print("7. The computer will also take its turn to guess your ships randomly.")
    print("8. The first player (either you or the computer) to sink all the ships wins "
          "the game.")
    print("9. You have a limited number of turns to sink all the computer's ships, and "
          "the computer will also try to sink yours.")
    print("10. The game ends when either you or the computer sinks all the ships.")
    print("11. Good luck! Enjoy the game!")

# Main menu for the game with replay option
def main_menu():
    print("\n" + "=" * 50)
    print(" " * 10 + "WELCOME TO BATTLESHIP" + " " * 10)
    print("=" * 50)
    
    player_name = input("\nPlease enter your name: ").strip()
    if not player_name:
        player_name = "Player"  # Default name if no input

    while True:
        print(f"\n{"=" * 50}")
        print("1. Start Game")
        print("2. How to Play")
        print("3. Exit")
        print("=" * 50)
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            while True:
                hits = play_battleship(player_name)
                replay = input("\nDo you want to play again? (yes/no): ").strip().lower()
                if replay == "no":
                    print(f"Thanks for playing, {player_name}! Your final score: {hits} hits!")
                    break
                elif replay != "yes":
                    print("Invalid choice. Please type 'yes' or 'no'.")
                else:
                    print("Restarting the game...\n")
        elif choice == "2":
            how_to_play()
        elif choice == "3":
            print(f"Goodbye, {player_name}!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the game
if __name__ == "__main__":
    main_menu()

