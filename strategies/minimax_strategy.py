from .abstract_strategy import AbstractStrategy


class MinimaxBasedStrategy(AbstractStrategy):
    
    def choose_best_guess(self, possible_words, attempts):
        
        if attempts == 0:
            return 'serai'  # Standard optimal first guess
        
        # If there's only one possibility, return it immediately
        if len(possible_words) == 1:
            return possible_words[0]
            
        best_worst_case = float('inf')
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
            
            # Find the worst-case scenario for this candidate
            worst_case = max(len(words) for words in feedback_patterns.values())
            
            # If this candidate's worst case is better than our best so far
            if worst_case < best_worst_case:
                best_worst_case = worst_case
                best_guess = candidate_word
                
        print(f"Best guess: {best_guess}")
        return best_guess