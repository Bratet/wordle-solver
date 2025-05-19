from abc import ABC, abstractmethod
from typing import List, Set, Optional, Tuple
from pathlib import Path

# Constants
DEFAULT_WORD_LENGTH = 5
DEFAULT_MAX_ATTEMPTS = 6
FEEDBACK_GREEN = "G"
FEEDBACK_YELLOW = "Y"
FEEDBACK_GRAY = "_"

class AbstractStrategy(ABC):
    """
    Abstract base class for Wordle solving strategies.
    
    This class provides common functionality for all Wordle solving strategies,
    including feedback generation and word space reduction.
    
    Attributes:
        vocabulary (List[str]): List of allowed words
        previous_guesses (Set[str]): Set of words already guessed
    """
    
    def __init__(self, vocabulary: str = 'data/allowed_words.txt') -> None:
        """
        Initialize the strategy with a vocabulary of allowed words.
        
        Args:
            vocabulary: Path to file containing allowed words
        """
        self.vocabulary = self._load_vocabulary(vocabulary)
        self.previous_guesses: Set[str] = set()
    
    @staticmethod
    def _load_vocabulary(file_path: str) -> List[str]:
        """
        Load vocabulary from a file.
        
        Args:
            file_path: Path to the vocabulary file
            
        Returns:
            List of words from the file
        """
        with open(file_path, 'r') as file:
            return [line.strip().lower() for line in file]
    
    def _generate_feedback(self, guess: str, target_word: str) -> str:
        """
        Generate feedback for a guess against a target word.
        
        Args:
            guess: The word that was guessed
            target_word: The target word to guess
            
        Returns:
            String of feedback indicators:
            - "G": correct letter, correct position
            - "Y": correct letter, wrong position
            - "_": letter not in word
        """
        guess = guess.lower()
        target_word = target_word.lower()
        
        feedback = [FEEDBACK_GRAY] * DEFAULT_WORD_LENGTH
        
        # Count occurrences of each letter in the target word
        letter_count: dict[str, int] = {}
        for char in target_word:
            letter_count[char] = letter_count.get(char, 0) + 1
        
        # First pass: Mark correct positions
        for i in range(DEFAULT_WORD_LENGTH):
            if guess[i] == target_word[i]:
                feedback[i] = FEEDBACK_GREEN
                letter_count[guess[i]] -= 1
        
        # Second pass: Mark correct letters in wrong positions
        for i in range(DEFAULT_WORD_LENGTH):
            if (feedback[i] == FEEDBACK_GRAY and 
                guess[i] in letter_count and 
                letter_count[guess[i]] > 0):
                feedback[i] = FEEDBACK_YELLOW
                letter_count[guess[i]] -= 1
        
        return ''.join(feedback)
    
    def _reduce_words_space(
        self,
        guess: str,
        possible_words: List[str],
        feedback: str
    ) -> List[str]:
        """
        Reduce the possible words space based on feedback from a guess.
        
        Args:
            guess: The word that was guessed
            possible_words: List of possible words before this guess
            feedback: Feedback string for the guess (e.g. "G_Y__")
            
        Returns:
            Reduced list of possible words
        """
        guess = guess.lower()
        new_word_space = possible_words.copy()
        
        # First pass: Handle green matches
        for i, sign in enumerate(feedback):
            if sign == FEEDBACK_GREEN:
                new_word_space = [word for word in new_word_space if guess[i] == word[i]]
        
        # Second pass: Handle yellow matches
        for i, sign in enumerate(feedback):
            if sign == FEEDBACK_YELLOW:
                new_word_space = [word for word in new_word_space if 
                                (guess[i] in word and guess[i] != word[i])]
        
        # Third pass: Handle gray matches
        gray_letters = {guess[i] for i, sign in enumerate(feedback) if sign == FEEDBACK_GRAY}
        
        for gray_letter in gray_letters:
            # Count occurrences as green or yellow
            green_yellow_count = sum(1 for i, sign in enumerate(feedback) 
                                if (sign == FEEDBACK_GREEN or sign == FEEDBACK_YELLOW) 
                                and guess[i] == gray_letter)
            
            if green_yellow_count == 0:
                # Letter not in word at all
                new_word_space = [word for word in new_word_space if gray_letter not in word]
            else:
                # Letter appears exactly green_yellow_count times
                new_word_space = [word for word in new_word_space 
                                if word.count(gray_letter) == green_yellow_count]
        
        return new_word_space
           
    def solve(self, game) -> Tuple[Optional[str], int]:
        """
        Solve the Wordle game using the strategy.
        
        Args:
            game: Wordle game instance to solve
            
        Returns:
            Tuple containing:
            - The winning word (or None if not solved)
            - Number of attempts made
        """
        possible_words = self.vocabulary.copy()
        attempts = 0
        self.previous_guesses = set()
        
        while attempts < DEFAULT_MAX_ATTEMPTS:
            guess = self.choose_best_guess(possible_words, attempts)
            
            # Add to our set of previous guesses BEFORE making the guess
            self.previous_guesses.add(guess)
            attempts += 1 
            
            is_correct, feedback, error_msg = game.make_guess(guess)
            
            if error_msg:
                print(f"Error: {error_msg}")
                continue
                
            if is_correct:
                return guess, attempts
            
            # Reduce the search space based on feedback
            possible_words = self._reduce_words_space(guess, possible_words, feedback)
            
            if not possible_words:
                print("Error: No possible words left in the word space!")
                return None, attempts
                
            # If only one word remains and we still have attempts, just guess it
            if len(possible_words) == 1 and attempts < DEFAULT_MAX_ATTEMPTS:
                final_guess = possible_words[0]
                
                # Skip if we already tried this word
                if final_guess in self.previous_guesses and final_guess != guess:
                    continue
                    
                self.previous_guesses.add(final_guess)
                attempts += 1
                is_correct, _, error_msg = game.make_guess(final_guess)
                
                if is_correct:
                    return final_guess, attempts
                else:
                    break
        
        return None, attempts
    
    @abstractmethod
    def choose_best_guess(self, possible_words: List[str], attempts: int) -> str:
        """
        Choose the best word to guess from the possible words.
        
        Args:
            possible_words: List of possible words to choose from
            attempts: Current number of attempts made
            
        Returns:
            The chosen word to guess
        """
        pass

