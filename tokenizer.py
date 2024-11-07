import re

def tokenize(text):
    # Regular expression to handle:
    # 1. Abbreviations (e.g., U.S.A)
    # 2. Words with internal hyphens (e.g., ice-cream)
    # 3. Contractions (e.g., isn't -> is, n't)
    # 4. Standard words, punctuation, and symbols
    token_pattern = r'''
        \b(?:[A-Za-z]\.){2,}             # Match abbreviations like U.S.A
        | \b\w+(?:-\w+)+\b               # Match hyphenated words like ice-cream
        | \b\w+n't\b                     # Match contractions like isn't, weren't
        | \b\w+'\w+\b                    # Match other contractions like you're, I'm
        | \b\w+\b                        # Match normal words
        | [\.,!?;:\(\)\[\]{}]            # Match punctuation as separate tokens
        | [^\w\s]                        # Match any other symbol as a separate token
    '''

    # Compile the regular expression pattern with verbose flag
    pattern = re.compile(token_pattern, re.VERBOSE)

    # Use findall to match all tokens according to the pattern
    tokens = pattern.findall(text)

    # Further split contractions like "isn't" into "is" and "n't"
    processed_tokens = []
    for token in tokens:
        if re.match(r"\b\w+n't\b", token):
            # Separate "n't" from the word (e.g., "isn't" -> "is", "n't")
            processed_tokens.append(token[:-3])  # The base word (e.g., "is")
            processed_tokens.append("n't")       # The "n't" part
        else:
            processed_tokens.append(token)

    return processed_tokens

# Prompt the user for input text
text = input("Enter the text to tokenize: ")
tokens = tokenize(text)
print(tokens)
