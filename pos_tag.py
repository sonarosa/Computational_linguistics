import numpy as np

# Define transition probabilities (a_ij)
transition_probs = {
    "START": {"NN": 0.5, "VB": 0.25, "JJ": 0.25, "RB": 0},
    "NN": {"STOP": 0.25, "NN": 0.25, "VB": 0.5, "JJ": 0, "RB": 0},
    "VB": {"STOP": 0.25, "NN": 0.25, "VB": 0, "JJ": 0.25, "RB": 0.25},
    "JJ": {"STOP": 0, "NN": 0.75, "VB": 0, "JJ": 0.25, "RB": 0},
    "RB": {"STOP": 0.5, "NN": 0.25, "VB": 0.25, "JJ": 0, "RB": 0},
}

# Define emission probabilities (b_ik)
emission_probs = {
    "NN": {"time": 0.1, "flies": 0.01, "fast": 0.01},
    "VB": {"time": 0.01, "flies": 0.1, "fast": 0.01},
    "JJ": {"time": 0, "flies": 0, "fast": 0.1},
    "RB": {"time": 0, "flies": 0, "fast": 0.1},
}

# Define the sentence
sentence = ["time", "flies", "fast"]

# Initialize Viterbi table and backpointer
tags = list(emission_probs.keys())
n = len(sentence)
m = len(tags)
viterbi = np.zeros((m, n))
backpointer = np.zeros((m, n), dtype=int)

# Initialization step
for i, tag in enumerate(tags):
    viterbi[i, 0] = transition_probs["START"].get(tag, 0) * emission_probs[tag].get(sentence[0], 0)

# Recursion step
for t in range(1, n):
    for i, tag in enumerate(tags):
        max_prob = 0
        max_state = 0
        for j, prev_tag in enumerate(tags):
            prob = viterbi[j, t - 1] * transition_probs[prev_tag].get(tag, 0) * emission_probs[tag].get(sentence[t], 0)
            if prob > max_prob:
                max_prob = prob
                max_state = j
        viterbi[i, t] = max_prob
        backpointer[i, t] = max_state

# Termination step
max_prob = 0
last_state = 0
for i, tag in enumerate(tags):
    prob = viterbi[i, n - 1] * transition_probs[tag].get("STOP", 0)
    if prob > max_prob:
        max_prob = prob
        last_state = i

# Backtracking
tags_sequence = []
current_state = last_state
for t in range(n - 1, -1, -1):
    tags_sequence.insert(0, tags[current_state])
    current_state = backpointer[current_state, t]

# Output the result
print("Most probable POS tag sequence:", tags_sequence)
