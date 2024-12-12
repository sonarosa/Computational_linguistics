import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter, defaultdict

# Preprocess documents by tokenizing
def preprocess(documents):
    tokenized_docs = [doc.lower().split() for doc in documents]
    return tokenized_docs

# Build co-occurrence matrix
def build_cooccurrence_matrix(tokenized_docs, window_size=2):
    vocab = set(word for doc in tokenized_docs for word in doc)
    vocab = sorted(vocab)
    word_to_id = {word: i for i, word in enumerate(vocab)}

    cooccurrence = np.zeros((len(vocab), len(vocab)))

    for doc in tokenized_docs:
        for i, word in enumerate(doc):
            word_id = word_to_id[word]
            start = max(i - window_size, 0)
            end = min(i + window_size + 1, len(doc))

            for j in range(start, end):
                if i != j:
                    context_word_id = word_to_id[doc[j]]
                    cooccurrence[word_id, context_word_id] += 1

    return cooccurrence, vocab

# Compute PPMI matrix
def compute_ppmi_matrix(cooccurrence):
    total_count = np.sum(cooccurrence)
    word_sums = np.sum(cooccurrence, axis=1)
    ppmi = np.zeros_like(cooccurrence)

    for i in range(cooccurrence.shape[0]):
        for j in range(cooccurrence.shape[1]):
            p_ij = cooccurrence[i, j] / total_count
            p_i = word_sums[i] / total_count
            p_j = word_sums[j] / total_count

            if p_ij > 0:
                ppmi[i, j] = max(np.log2(p_ij / (p_i * p_j)), 0)

    return ppmi

# Calculate cosine similarity
def calculate_cosine_similarity(matrix, item1, item2, vocab):
    if item1 not in vocab or item2 not in vocab:
        raise ValueError(f"'{item1}' or '{item2}' is not in the vocabulary.")

    word_to_id = {word: i for i, word in enumerate(vocab)}
    vector1 = matrix[word_to_id[item1]].reshape(1, -1)
    vector2 = matrix[word_to_id[item2]].reshape(1, -1)

    similarity = cosine_similarity(vector1, vector2)[0][0]
    return similarity

# Example usage
if __name__ == "__main__":
    documents = [
        "the cat sat on the mat",
        "the dog barked at the mailman",
        "the cat and the dog became friends",
    ]

    tokenized_docs = preprocess(documents)
    cooccurrence, vocab = build_cooccurrence_matrix(tokenized_docs)
    ppmi_matrix = compute_ppmi_matrix(cooccurrence)

    print("Vocabulary:", vocab)
    print("\nPPMI Matrix:")
    print(ppmi_matrix)

    word1, word2 = "cat", "dog"
    similarity = calculate_cosine_similarity(ppmi_matrix, word1, word2, vocab)
    print(f"\nCosine similarity between '{word1}' and '{word2}': {similarity:.4f}")
