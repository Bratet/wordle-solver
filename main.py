from wordle import Wordle
from utils import print_colored_feedback


def play_wordle_cli():
    """Play Wordle in the command line"""
    # Create a game instance
    game = Wordle()
    
    print(f"Welcome to Wordle! Guess the {game.word_length}-letter word in {game.max_attempts} attempts.")
    print("After each guess, you'll get feedback:")
    print("  🟩 = correct letter in correct position")
    print("  🟨 = correct letter in wrong position")
    print("  ⬛ = letter not in word")
    print(f"Target word (for testing): {game.target_word}")  # Remove this line in the final version
    
    while True:
        state = game.get_game_state()
        
        # Print previous guesses and feedback
        for i, (guess, feedback) in enumerate(zip(state["guesses"], state["feedbacks"])):
            print(f"Guess {i+1}: {print_colored_feedback(guess, feedback)}")
        
        # Check if game is over
        if state["game_over"]:
            if state["won"]:
                print(f"Congratulations! You guessed the word: {game.target_word.upper()}")
            else:
                print(f"Game over! The word was: {game.target_word.upper()}")
            
            play_again = input("Play again? (y/n): ").lower()
            if play_again != 'y':
                break
            game.reset_game()
            print("\nNew game started!")
            print(f"Target word (for testing): {game.target_word}")  # Remove this line in the final version
            continue
        
        # Get next guess
        guess = input(f"\nEnter guess {state['attempts']+1}/{game.max_attempts}: ").lower()
        
        # Process guess
        is_correct, feedback, error = game.make_guess(guess)
        
        # If there's an error, show the message and let the user try again
        if error:
            print(f"Error: {error}")
            continue
            
        # Immediately show feedback after a valid guess
        print(f"Feedback: {print_colored_feedback(guess, feedback)}")

if __name__ == "__main__":
    play_wordle_cli()