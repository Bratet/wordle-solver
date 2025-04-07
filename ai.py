import numpy as np

class WordleAI:
    def __init__(self, vocabulary='wordle_dictionary.txt'):
        with open(vocabulary, 'r') as file:
            self.vocabulary = [line.strip() for line in file]

    def get_possible_words(self, state):
        return [word for word in self.vocabulary if self.is_valid_guess(word, state)]
        