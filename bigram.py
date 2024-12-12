import nltk
from nltk.tokenize import word_tokenize
from nltk.util import bigrams
from collections import Counter, defaultdict

# Download necessary NLTK data
nltk.download('punkt')

# Function to calculate bigram probabilities
def calculate_bigram_probabilities(corpus):
    # Tokenize the corpus
    tokens = word_tokenize(corpus)

    # Generate bigrams
    bigram_list = list(bigrams(tokens))

    # Count unigrams and bigrams
    unigram_counts = Counter(tokens)
    bigram_counts = Counter(bigram_list)

    # Calculate bigram probabilities
    bigram_probabilities = {}
    for bigram, count in bigram_counts.items():
        bigram_probabilities[bigram] = count / unigram_counts[bigram[0]]

    return bigram_probabilities

# Function to calculate the probability of a given sentence
def calculate_sentence_probability(sentence, bigram_probabilities):
    tokens = word_tokenize(sentence)
    sentence_bigrams = list(bigrams(tokens))

    probability = 1.0
    for bigram in sentence_bigrams:
        if bigram in bigram_probabilities:
            probability *= bigram_probabilities[bigram]
        else:
            # Assign a small probability for unseen bigrams (smoothing)
            probability *= 1e-6

    return probability

# Sample corpus
corpus = "You are learning from Geeks for Geeks. Geeks for Geeks is a great platform."

# Calculate bigram probabilities
bigram_probabilities = calculate_bigram_probabilities(corpus)

# Print bigram probabilities
print("Bigram Probabilities:")
for bigram, prob in bigram_probabilities.items():
    print(f"{bigram}: {prob:.6f}")

# Sample sentence
sentence = "You are learning from Geeks"

# Calculate sentence probability
sentence_probability = calculate_sentence_probability(sentence, bigram_probabilities)

print(f"\nProbability of the sentence '{sentence}': {sentence_probability:.6e}")
