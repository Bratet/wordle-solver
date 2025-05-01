from .abstract_strategy import AbstractStrategy
from collections import defaultdict

class FrequencyBasedStrategy(AbstractStrategy):
    
    def choose_best_guess(self, possible_words, attempts):
        
        if attempts == 0:
            return 'cares' # pre-computed optimal first guess
        
        # If there's only one possibility, return it immediately
        if len(possible_words) == 1:
            return possible_words[0]
        
        # Calculate letter frequencies in each position
        position_frequencies = [defaultdict(int) for _ in range(5)]
        
        # Count frequency of each letter at each position
        for word in possible_words:
            for position, letter in enumerate(word):
                position_frequencies[position][letter] += 1
        
        best_score = -1
        best_guess = None
        
        # Consider ALL vocabulary words as potential guesses
        # but skip words we've already guessed
        for candidate_word in self.vocabulary:
            
            # Skip words we've already guessed
            if candidate_word in self.previous_guesses:
                continue
            
            # Calculate score based on position-specific letter frequencies
            score = 0
            seen_letters = set()  # To track duplicate letters
            
            for position, letter in enumerate(candidate_word):
                # Add position-specific frequency
                score += position_frequencies[position][letter]
                
                # Optional: Penalize duplicate letters
                if letter in seen_letters:
                    score *= 0.8  # Reduce score for duplicate letters
                seen_letters.add(letter)
            
            # Update best guess if this one has a higher score
            if score > best_score:
                best_score = score
                best_guess = candidate_word

        return best_guess