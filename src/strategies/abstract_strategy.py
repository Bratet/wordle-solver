from abc import ABC, abstractmethod

class AbstractStrategy(ABC):
    def __init__(self, vocabulary='data/allowed_words.txt'):
        with open(vocabulary, 'r') as file:
            # Convert all words to lowercase for consistent comparison
            self.vocabulary = [line.strip().lower() for line in file]
            
        # Initialize previous guesses tracking
        self.previous_guesses = set()
    
    def _generate_feedback(self, guess: str, target_word:str):
        """
        Generate feedback for a guess:
        - "G": correct letter, correct position
        - "Y": correct letter, wrong position
        - "_": letter not in word
        
        Ensures case-insensitive comparison
        """
        # Convert both words to lowercase for consistent comparison
        guess = guess.lower()
        target_word = target_word.lower()
        
        word_length = 5
        feedback = ["_"] * word_length
        
        # Count occurrences of each letter in the target word
        letter_count = {}
        for char in target_word:
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
        
        # First pass: Mark correct positions
        for i in range(word_length):
            if guess[i] == target_word[i]:
                feedback[i] = "G"
                letter_count[guess[i]] -= 1
        
        # Second pass: Mark correct letters in wrong positions
        for i in range(word_length):
            if feedback[i] == "_" and guess[i] in letter_count and letter_count[guess[i]] > 0:
                feedback[i] = "Y"
                letter_count[guess[i]] -= 1
        
        return ''.join(feedback)
    
    
    def _reduce_words_space(self, guess, possible_words, feedback):
        """
        Reduce the possible words space after getting feedback from a guess in Wordle.
        
        Args:
            guess (str): The word that was guessed (converted to lowercase)
            possible_words (list): List of possible words before this guess
            feedback (list): Feedback for each letter, e.g. ['_', 'Y', 'G', '_', '_']
                            'G' = Green (correct letter, correct position)
                            'Y' = Yellow (correct letter, wrong position)
                            '_' = Gray (letter not in word)
        
        Returns:
            list: Reduced list of possible words
        """
        # Convert guess to lowercase for consistency
        guess = guess.lower()
        new_word_space = possible_words.copy()
        
        # First pass: Handle 'G' (green) matches
        for i, sign in enumerate(feedback):
            if sign == 'G':
                new_word_space = [word for word in new_word_space if guess[i] == word[i]]
        
        # Second pass: Handle 'Y' (yellow) matches
        for i, sign in enumerate(feedback):
            if sign == 'Y':
                # Letter is in the word but not at this position
                new_word_space = [word for word in new_word_space if 
                                (guess[i] in word and guess[i] != word[i])]
        
        # Third pass: Handle '_' (gray/blank) - letter not in word
        # We need to be careful with this because duplicate letters
        # might be marked as gray if they appear more times in the guess
        # than in the actual word
        gray_letters = {guess[i] for i, sign in enumerate(feedback) if sign == '_'}
        
        # For each gray letter, we need to check if it appears elsewhere as green or yellow
        for gray_letter in gray_letters:
            # Count how many times this letter appears as green or yellow
            green_yellow_count = sum(1 for i, sign in enumerate(feedback) 
                                if (sign == 'G' or sign == 'Y') and guess[i] == gray_letter)
            
            # If it never appears as green or yellow, it's not in the word
            if green_yellow_count == 0:
                new_word_space = [word for word in new_word_space if gray_letter not in word]
            else:
                # If it appears as green or yellow, then the allowed count is exactly that number
                for word in new_word_space.copy():
                    if word.count(gray_letter) > green_yellow_count:
                        new_word_space.remove(word)
        
        return new_word_space
           
    def solve(self, game):
        possible_words = self.vocabulary.copy()
        attempts = 0
        self.previous_guesses = set()
        
        # Get the game's max attempts
        max_attempts = 6  # Standard Wordle limit
        
        while attempts < max_attempts:
            guess = self.choose_best_guess(possible_words, attempts)
            
            # Add to our set of previous guesses BEFORE making the guess
            self.previous_guesses.add(guess)
            
            attempts += 1 
            
            is_correct, feedback, error_msg = game.make_guess(guess)
            
            # Check for errors
            if error_msg:
                print(f"Error: {error_msg}")
                continue
                
            # Check for correct guess
            if is_correct:
                return guess, attempts
            
            # Reduce the search space based on feedback
            possible_words = self._reduce_words_space(guess, possible_words, feedback)
            
            # If we've run out of possible words, something went wrong
            if len(possible_words) == 0:
                print("Error: No possible words left in the word space!")
                return None, attempts
                
            # If only one word remains and we still have attempts, just guess it
            if len(possible_words) == 1 and attempts < max_attempts:
                final_guess = possible_words[0]
                
                # Skip if we already tried this word
                if final_guess in self.previous_guesses and final_guess != guess:
                    continue
                    
                # Otherwise make this our final guess
                self.previous_guesses.add(final_guess)
                attempts += 1
                is_correct, _, error_msg = game.make_guess(final_guess)
                
                if is_correct:
                    return final_guess, attempts
                else:
                    break
        
        return None, attempts
    
    @abstractmethod
    def choose_best_guess(self, possible_words, attempts):
        pass

