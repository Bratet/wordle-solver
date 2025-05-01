#!/usr/bin/env python3
"""
Interactive Wordle Solver
------------------------
This script allows users to input a target word and see how the entropy-based solver
attempts to solve it, showing the thought process and guesses along the way.
"""

from src.wordle import Wordle
from src.strategies import EntropyBasedStrategy, MinimaxBasedStrategy, FrequencyBasedStrategy, HybridStrategy


def get_valid_word(prompt: str, word_list: list) -> str:
    """Get a valid word from user input."""
    while True:
        word = input(prompt).strip().lower()
        if word in word_list:
            return word
        print(f"Invalid word. Please enter a valid 5-letter word from the allowed list.")


def main():
    # Initialize the game and strategy
    game = Wordle(allowed_words="data/allowed_words.txt", possible_words="data/possible_words.txt")
    
    # choose strategy
    strategy = HybridStrategy()
    
    # Load word lists
    with open("data/allowed_words.txt", "r") as f:
        allowed_words = [line.strip() for line in f]
    with open("data/possible_words.txt", "r") as f:
        possible_words = [line.strip() for line in f]
    
    print("Welcome to the Wordle Solver!")
    print("Enter a 5-letter word and watch the solver try to guess it.")
    print("The solver will show its thought process and guesses.\n")
    
    # Get target word from user
    target_word = get_valid_word(
        "Enter the target word (must be in the possible words list): ",
        possible_words
    )
    
    print(f"\nTarget word set to: {target_word.upper()}")
    print("Starting solver...\n")
    
    # Reset game with target word
    game.reset_game(target_word)
    
    # Run solver and show detailed output
    strategy.solve(game)
    
    # Display results
    print("\nSolver Results:")
    print(f"Target word: {target_word.upper()}")
    print(f"Number of attempts: {game.attempts}")
    print(f"Success: {'Yes' if game.attempts <= 6 else 'No'}")


if __name__ == "__main__":
    main()
