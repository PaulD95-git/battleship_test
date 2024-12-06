import random

# Create a game board
def create_board(size=5):
    return [["~" for _ in range(size)] for _ in range(size)]

# Print the game board with row and column numbers
def print_board(board):
    print("  " + " ".join(str(i) for i in range(len(board[0]))))  # Column numbers
    for idx, row in enumerate(board):
        print(f"{idx} " + " ".join(row))  # Row number and row content

# Place multiple ships (without overlapping)
def place_multiple_ships(board, ship_count=3):
    ships = []
    while len(ships) < ship_count:
        row = random.randint(0, len(board) - 1)
        col = random.randint(0, len(board[0]) - 1)
        if (row, col) not in ships:  # Avoid duplicate positions
            ships.append((row, col))
    return ships

# Get player's guess with input examples
def get_player_guess(board_size):
    while True:
        try:
            print(f"Enter a row (0 to {board_size - 1}) and column (0 to {board_size - 1}).")
            row = int(input("Guess Row: "))
            col = int(input("Guess Column: "))
            if 0 <= row < board_size and 0 <= col < board_size:
                return row, col
            else:
                print("Invalid input! Row and column must be within the range 0 to", board_size - 1)
        except ValueError:
            print("Invalid input! Please enter integers only.")

# Check if the guess is correct or already guessed
def check_guess(board, guess, ships, score, previous_guesses):
    row, col = guess

    if guess in previous_guesses:
        print("Invalid input! You've already guessed this location.")
        return False  # Return False to prevent using a turn
    
    if guess in ships:
        print("Hit! You sunk part of a battleship!")
        ships.remove(guess)  # Remove the hit ship
        board[row][col] = "H"  # Mark hit
        score['hits'] += 1
        previous_guesses.add(guess)  # Add the guess to the set of previous guesses
        if not ships:
            print("Congratulations! You sunk all the battleships!")
            return True
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

    board = create_board(board_size)
    ships = place_multiple_ships(board, ship_count)
    score = {'hits': 0, 'misses': 0}  # Track hits and misses
    previous_guesses = set()  # Store previously guessed locations

    print(f"\nWelcome to Battleship, {player_name}!")
    print(f"The board is {board_size}x{board_size}. There are {ship_count} battleships to sink.")
    print_board(board)

    for turn in range(turns):
        print(f"\nTurn {turn + 1}/{turns}")
        guess = get_player_guess(board_size)
        if check_guess(board, guess, ships, score, previous_guesses):
            break
        print_board(board)
    else:
        print("Game Over! The battleships were at:", ships)

    print("\nGame Over!")
    print(f"Final Score: {score['hits']} hits, {score['misses']} misses.")
    return score['hits']  # Return score to determine replay option

# Display how to play the game
def how_to_play():
    print("\nHow to Play Battleship:")
    print("1. The game board is a grid, represented by '~'.")
    print("2. Multiple battleships are hidden at random locations on the grid.")
    print("3. Each turn, you will guess a row and column (e.g., 2 3).")
    print("4. If you hit a battleship, it will be marked as 'H'.")
    print("5. If you miss, the grid will mark it with an 'X'.")
    print("6. You have a limited number of turns to sink all battleships. Good luck!")
    print()

# Main menu for the game with replay option
def main_menu():
    print("=== Welcome to Battleship ===")
    player_name = input("Please enter your name: ").strip()
    if not player_name:
        player_name = "Player"  # Default name if no input

    while True:
        print(f"\n=== Main Menu ===")
        print("1. Start Game")
        print("2. How to Play")
        print("3. Exit")
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






