import random
from typing import List, Tuple

class Wordle:
    def __init__(self, word_length=5, max_attempts=6):
        """Initialize the Wordle game with a list of words"""
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.attempts = 0
        self.guesses = []
        self.feedbacks = []
        
        # Use a small built-in list of words
        with open("wordle_dictionary.txt", "r") as file:
            self.word_list = [line.strip() for line in file]
        
        # Select a random target word
        self.target_word = random.choice(self.word_list)
        
    def reset_game(self):
        """Reset the game with a new word"""
        self.target_word = random.choice(self.word_list)
        self.attempts = 0
        self.guesses = []
        self.feedbacks = []
        
    def is_valid_word(self, word: str) -> bool:
        """Check if a word is valid (right length and in word list)"""
        return word.lower() in self.word_list
        
    def make_guess(self, guess: str) -> Tuple[bool, List[str], str]:
        """
        Process a guess and return:
        - Whether the guess is correct
        - Feedback as a list of colored positions
        - Error message if any
        """
        guess = guess.lower()
        
        # Check if the guess is valid
        if len(guess) != self.word_length:
            return False, [], "Invalid word length"
            
        if not guess.isalpha():
            return False, [], "Word contains non-alphabetic characters"
            
        if not self.is_valid_word(guess):
            return False, [], "Word not in dictionary"
            
        if self.attempts >= self.max_attempts:
            return False, [], "No more attempts allowed"
            
        # Record the guess
        self.attempts += 1
        self.guesses.append(guess)
        
        # Generate feedback
        feedback = self.generate_feedback(guess)
        self.feedbacks.append(feedback)
        
        # Check if the guess is correct
        is_correct = (guess == self.target_word)
        
        return is_correct, feedback, ""
    
    def generate_feedback(self, guess: str) -> List[str]:
        """
        Generate feedback for a guess:
        - "G": correct letter, correct position
        - "Y": correct letter, wrong position
        - "_": letter not in word
        """
        feedback = ["_"] * self.word_length
        
        # Count occurrences of each letter in the target word
        letter_count = {}
        for char in self.target_word:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
        
        # First pass: Mark correct positions
        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                feedback[i] = "G"
                letter_count[guess[i]] -= 1
        
        # Second pass: Mark correct letters in wrong positions
        for i in range(self.word_length):
            if feedback[i] == "_" and guess[i] in letter_count and letter_count[guess[i]] > 0:
                feedback[i] = "Y"
                letter_count[guess[i]] -= 1
        
        return feedback
    
    def get_game_state(self):
        """Return the current game state"""
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "guesses": self.guesses,
            "feedbacks": self.feedbacks,
            "game_over": self.attempts >= self.max_attempts or 
                         (self.guesses and self.guesses[-1] == self.target_word),
            "won": self.guesses and self.guesses[-1] == self.target_word
        }
    
    def get_target_word(self):
        """Get the target word (for debugging or when game is over)"""
        return self.target_word