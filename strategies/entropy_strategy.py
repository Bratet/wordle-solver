from .abstract_strategy import AbstractStrategy
import numpy as np


class EntropyBasedStrategy(AbstractStrategy):
    
    def choose_best_guess(self, possible_words, attempts):
        
        if attempts == 0:
            return 'tares'  # Standard optimal first guess
        
        # If there's only one possibility, return it immediately
        if len(possible_words) == 1:
            return possible_words[0]
            
        best_expected_entropy = -1
        best_guess = None
        
        # Consider ALL vocabulary words as potential guesses
        # but skip words we've already guessed
        for candidate_word in self.vocabulary:
            
            # Skip words we've already guessed
            if candidate_word in self.previous_guesses:
                continue
                
            feedback_patterns = {}
            
            # But only evaluate against remaining possible solutions
            for target_word in possible_words:
                pattern = self._generate_feedback(candidate_word, target_word)
                
                if pattern not in feedback_patterns:
                    feedback_patterns[pattern] = []
                feedback_patterns[pattern].append(target_word)
            
            # Calculate expected entropy
            expected_entropy = 0
                
            for pattern, remaining_words in feedback_patterns.items():
                probability = len(remaining_words) / len(possible_words)
                # Add a small epsilon to avoid log(0)
                expected_entropy -= probability * np.log2(probability + 1e-10)
            
            if expected_entropy > best_expected_entropy:
                best_guess = candidate_word
                best_expected_entropy = expected_entropy
                
        return best_guess