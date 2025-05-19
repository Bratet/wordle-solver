import random
from typing import List, Tuple, Dict, Optional
from pathlib import Path

# Constants
DEFAULT_WORD_LENGTH = 5
DEFAULT_MAX_ATTEMPTS = 6
FEEDBACK_GREEN = "G"
FEEDBACK_YELLOW = "Y"
FEEDBACK_GRAY = "_"

class Wordle:
    """
    A class representing the Wordle game.
    
    Attributes:
        word_length (int): Length of words in the game
        max_attempts (int): Maximum number of allowed attempts
        attempts (int): Current number of attempts made
        guesses (List[str]): List of words guessed so far
        feedbacks (List[List[str]]): List of feedback for each guess
        word_list (List[str]): List of allowed words
        target_word_list (List[str]): List of possible target words
        target_word (str): The current target word to guess
    """
    
    def __init__(
        self,
        word_length: int = DEFAULT_WORD_LENGTH,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        target_word: Optional[str] = None,
        allowed_words: Optional[str] = None,
        possible_words: Optional[str] = None
    ) -> None:
        """
        Initialize the Wordle game.
        
        Args:
            word_length: Length of words in the game
            max_attempts: Maximum number of allowed attempts
            target_word: Specific target word to use (if None, random word is chosen)
            allowed_words: Path to file containing allowed words
            possible_words: Path to file containing possible target words
        """
        self.word_length = word_length
        self.max_attempts = max_attempts
        self.attempts = 0
        self.guesses: List[str] = []
        self.feedbacks: List[List[str]] = []
        
        # Load word lists
        if allowed_words is None or possible_words is None:
            raise ValueError("Both allowed_words and possible_words file paths must be provided")
            
        self.word_list = self._load_word_list(allowed_words)
        self.target_word_list = self._load_word_list(possible_words)
        
        # Set target word
        self.target_word = target_word if target_word is not None else random.choice(self.target_word_list)
    
    @staticmethod
    def _load_word_list(file_path: str) -> List[str]:
        """
        Load words from a file.
        
        Args:
            file_path: Path to the file containing words
            
        Returns:
            List of words from the file
        """
        with open(file_path, "r") as file:
            return [line.strip().lower() for line in file]
            
    def reset_game(self, target_word: Optional[str] = None) -> None:
        """
        Reset the game with a new word.
        
        Args:
            target_word: New target word to use (if None, random word is chosen)
        """
        self.target_word = target_word if target_word is not None else random.choice(self.target_word_list)
        self.attempts = 0
        self.guesses = []
        self.feedbacks = []
        
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a word is valid.
        
        Args:
            word: Word to check
            
        Returns:
            True if the word is valid (right length and in word list), False otherwise
        """
        return len(word) == self.word_length and word.lower() in self.word_list
        
    def make_guess(self, guess: str) -> Tuple[bool, List[str], str]:
        """
        Process a guess and return feedback.
        
        Args:
            guess: Word to guess
            
        Returns:
            Tuple containing:
            - Whether the guess is correct
            - Feedback as a list of colored positions
            - Error message if any
        """
        guess = guess.lower()
        
        # Validate guess
        if len(guess) != self.word_length:
            return False, [], f"Word must be {self.word_length} letters long"
            
        if not guess.isalpha():
            return False, [], "Word must contain only letters"
            
        if not self.is_valid_word(guess):
            return False, [], "Word not in dictionary"
            
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
        Generate feedback for a guess.
        
        Args:
            guess: Word that was guessed
            
        Returns:
            List of feedback indicators:
            - "G": correct letter, correct position
            - "Y": correct letter, wrong position
            - "_": letter not in word
        """
        feedback = [FEEDBACK_GRAY] * self.word_length
        
        # Count occurrences of each letter in the target word
        letter_count: Dict[str, int] = {}
        for char in self.target_word:
            letter_count[char] = letter_count.get(char, 0) + 1
        
        # First pass: Mark correct positions
        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                feedback[i] = FEEDBACK_GREEN
                letter_count[guess[i]] -= 1
        
        # Second pass: Mark correct letters in wrong positions
        for i in range(self.word_length):
            if (feedback[i] == FEEDBACK_GRAY and 
                guess[i] in letter_count and 
                letter_count[guess[i]] > 0):
                feedback[i] = FEEDBACK_YELLOW
                letter_count[guess[i]] -= 1
        
        return feedback
    
    def get_game_state(self) -> Dict:
        """
        Get the current game state.
        
        Returns:
            Dictionary containing:
            - attempts: Current number of attempts
            - max_attempts: Maximum allowed attempts
            - guesses: List of words guessed
            - feedbacks: List of feedback for each guess
            - game_over: Whether the game is over
            - won: Whether the game was won
        """
        return {
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "guesses": self.guesses,
            "feedbacks": self.feedbacks,
            "game_over": (self.attempts >= self.max_attempts or 
                         (self.guesses and self.guesses[-1] == self.target_word)),
            "won": self.guesses and self.guesses[-1] == self.target_word
        }
