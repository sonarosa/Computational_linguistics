

import re
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')

class BigramSpellChecker:
    def __init__(self, corpus):
        self.corpus = corpus.lower()
        self.vocabulary = set()
        self.unigrams = Counter()
        self.bigrams = Counter()
        self.create_vocabulary_and_bigrams()

    def create_vocabulary_and_bigrams(self):
        tokens = word_tokenize(self.corpus)
        self.vocabulary = set(tokens)
        self.unigrams = Counter(tokens)
        self.bigrams = Counter(ngrams(tokens, 2))

    def is_word_in_vocab(self, word):
        return word in self.vocabulary

    def edit_distance_one(self, word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edit_distance_two(self, word):
        return set(e2 for e1 in self.edit_distance_one(word) for e2 in self.edit_distance_one(e1))

    def bigram_probability(self, w1, w2, alpha=1):
        bigram_count = self.bigrams[(w1, w2)]
        unigram_count = self.unigrams[w1]
        vocabulary_size = len(self.vocabulary)
        return (bigram_count + alpha) / (unigram_count + alpha * vocabulary_size)

    def get_candidates(self, word):
        candidates = [w for w in self.edit_distance_one(word) if self.is_word_in_vocab(w)]
        if not candidates:
            candidates = [w for w in self.edit_distance_two(word) if self.is_word_in_vocab(w)]
        return candidates

    def correct_article(self, prev_word, next_word, misspelled_word):
        if misspelled_word in ["a", "an"]:
            if next_word and next_word[0] in "aeiou":
                return "an"
            else:
                return "a"
        return misspelled_word

    def suggest_correction(self, prev_words, misspelled_word):
        candidates = self.get_candidates(misspelled_word)
        if not candidates:
            return misspelled_word
        best_candidate = max(
            candidates,
            key=lambda word: self.bigram_probability(prev_words[-2], word) + self.bigram_probability(prev_words[-1], word),
            default=misspelled_word
        )
        return best_candidate

    def correct_text(self, text):
        tokens = word_tokenize(text.lower())
        corrected_text = []

        for i, word in enumerate(tokens):
            if not self.is_word_in_vocab(word):
                prev_words = tokens[max(0, i-2):i]
                if i < len(tokens) - 1:
                    next_word = tokens[i + 1]
                else:
                    next_word = ""

                if word in ["a", "an"]:
                    corrected_word = self.correct_article(prev_words[-1] if prev_words else "", next_word, word)
                else:
                    corrected_word = self.suggest_correction(prev_words, word)

                corrected_text.append(corrected_word)
            else:
                corrected_text.append(word)

        return ' '.join(corrected_text)

corpus = """This is a simple example corpus with enough text to cover basic English words
and some example sentences to provide a context for bigrams and vocabulary.
Ideally, you would use a larger English corpus here."""
spell_checker = BigramSpellChecker(corpus)

text_to_correct = "This is an exmple text with mre errors."
corrected_text = spell_checker.correct_text(text_to_correct)
print("Corrected Text:", corrected_text)
