import random
def get_difficulty():
    """Get difficulty level from user."""
    print("\nSelect difficulty level:")
    print("1. Easy (1-50)")
    print("2. Medium (1-100)")
    print("3. Hard (1-200)")
    
    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice == 1:
                return 50
            elif choice == 2:
                return 100
            elif choice == 3:
                return 200
            else:
                print("Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_round(max_number):
    """Play a single round of the guessing game."""
    number = random.randint(1, max_number)
    attempts = 0
    hints_used = 0
    
    print(f"\nI'm thinking of a number between 1 and {max_number}.")
    print("Type 'hint' for a hint or 'quit' to exit.\n")
    
    while True:
        try:
            user_input = input("Enter your guess: ").strip().lower()
            
            if user_input == 'quit':
                print(f"The number was {number}. Thanks for playing!")
                return None
            
            if user_input == 'hint':
                if hints_used < 2:
                    hints_used += 1
                    hint = random.randint(1, max_number)
                    print(f"Hint: Try a number between {min(number, hint)} and {max(number, hint)}")
                else:
                    print("No more hints available!")
                continue
            
            guess = int(user_input)
            
            if guess < 1 or guess > max_number:
                print(f"Please enter a number between 1 and {max_number}.")
                continue
            
            attempts += 1
            
            if guess < number:
                print("Too low! Try again.")
            elif guess > number:
                print("Too high! Try again.")
            else:
                print(f"Correct! You guessed it in {attempts} attempts!")
                return attempts
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def number_guessing_game():
    """Main game loop."""
    print("=" * 50)
    print("Welcome to the Number Guessing Game!")
    print("=" * 50)
    
    games_played = 0
    best_score = float('inf')
    
    while True:
        max_number = get_difficulty()
        score = play_round(max_number)
        
        if score is not None:
            games_played += 1
            if score < best_score:
                best_score = score
            
            print(f"\nStats: Games played: {games_played}, Best score: {best_score}")
        
        play_again = input("\nPlay again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print(f"\nThanks for playing! You played {games_played} game(s).")
            if games_played > 0:
                print(f"Your best score was {best_score} attempts.")
            break

if __name__ == "__main__":
    number_guessing_game()