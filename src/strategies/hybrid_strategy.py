from .abstract_strategy import AbstractStrategy
from collections import defaultdict
import numpy as np

class HybridStrategy(AbstractStrategy):
    
    def choose_best_guess(self, possible_words, attempts):
        
        if attempts == 0:
            return 'tares' # pre-computed optimal first guess
        
        # If there's only one possibility, return it immediately
        if len(possible_words) == 1:
            return possible_words[0]
        
        # Calculate letter frequencies in each position
        position_frequencies = [defaultdict(int) for _ in range(5)]
        
        # Count frequency of each letter at each position
        for word in possible_words:
            for position, letter in enumerate(word):
                position_frequencies[position][letter] += 1
        
        best_hybrid_score = -1
        best_guess = None
        
        # Store scores for all candidates for normalization
        frequency_scores = []
        entropy_scores = []
        candidate_words = []
        
        for candidate_word in self.vocabulary:
            
            # Skip words we've already guessed
            if candidate_word in self.previous_guesses:
                continue
            
            feedback_patterns = {}
            
            # But only evaluate against remaining possible solutions
            for target_word in possible_words:
                pattern = self._generate_feedback(candidate_word, target_word)
                
                if pattern not in feedback_patterns:
                    feedback_patterns[pattern] = 0
                feedback_patterns[pattern] += 1
                
            # Calculate expected entropy
            expected_entropy = 0
                
            for pattern, num_remaining_words in feedback_patterns.items():
                probability = num_remaining_words / len(possible_words)
                # Add a small epsilon to avoid log(0)
                expected_entropy -= probability * np.log2(probability + 1e-10)
            
            # Calculate score based on position-specific letter frequencies
            frequency_score = 0
            seen_letters = set()  # To track duplicate letters
            
            for position, letter in enumerate(candidate_word):
                # Add position-specific frequency
                frequency_score += position_frequencies[position][letter]
                
                # Optional: Penalize duplicate letters
                if letter in seen_letters:
                    frequency_score *= 0.8  # Reduce score for duplicate letters
                seen_letters.add(letter)
                
            # Store the scores for later normalization
            frequency_scores.append(frequency_score)
            entropy_scores.append(expected_entropy)
            candidate_words.append(candidate_word)
        
            
        # Normalize frequency scores (higher is better)
        min_freq = min(frequency_scores)
        max_freq = max(frequency_scores)
        if max_freq > min_freq:
            normalized_freq_scores = [(score - min_freq) / (max_freq - min_freq) for score in frequency_scores]
        else:
            normalized_freq_scores = [1.0] * len(frequency_scores)
            
        # Normalize entropy scores (higher is better)
        min_entropy = min(entropy_scores)
        max_entropy = max(entropy_scores)
        if max_entropy > min_entropy:
            normalized_entropy_scores = [(score - min_entropy) / (max_entropy - min_entropy) for score in entropy_scores]
        else:
            normalized_entropy_scores = [1.0] * len(entropy_scores)
        
        # Dynamically adjust weights based on the number of attempts (0-5)
        entropy_weight = max(0.7 - (attempts * 0.1), 0.1)    # Decreases from 0.7 to 0.1
        frequency_weight = min(0.3 + (attempts * 0.1), 0.9)   # Increases from 0.3 to 0.9
        
        # Ensure weights sum to 1.0
        total = entropy_weight + frequency_weight
        entropy_weight /= total
        frequency_weight /= total
        
        # Calculate hybrid scores using normalized values
        for i, candidate_word in enumerate(candidate_words):
            hybrid_score = (
                frequency_weight * normalized_freq_scores[i] + 
                entropy_weight * normalized_entropy_scores[i]
            )
            
            # Update best guess if this one has a higher score
            if hybrid_score > best_hybrid_score:
                best_hybrid_score = hybrid_score
                best_guess = candidate_word
                
        return best_guess