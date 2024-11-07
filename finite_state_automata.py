def fsa_plural_noun():
    """
    FSA that validates whether a user-inputted word is a correctly pluralized noun ending with 'y'.
    It accepts words ending with "ys" after a vowel and "ies" after a consonant.
    """
    vowels = {'a', 'e', 'i', 'o', 'u'}
    consonants = set("bcdfghjklmnpqrstvwxyz")

    # Get user input
    word = input("Enter a plural noun ending with 'y' to check: ").strip().lower()

    # Initial state (q0)
    current_state = 'q0'

    # Transition to state q1 if word meets minimum length
    if len(word) < 3:
        print("Rejected: Word is too short to be a valid plural noun.")
        return False

    # Move to state q1 to check suffix
    current_state = 'q1'

    if current_state == 'q1':
        # Check if the word ends with "ies"
        if word.endswith("ies"):
            # If it ends with a consonant + "ies", move to q2 (accepting state)
            if len(word) > 3 and word[-4] in consonants:
                current_state = 'q2'
            else:
                current_state = 'q0'  # Move back to rejection if invalid

        # Check if the word ends with "ys"
        elif word.endswith("ys"):
            # If it ends with a vowel + "ys", move to q3 (accepting state)
            if len(word) > 2 and word[-3] in vowels:
                current_state = 'q3'
            else:
                current_state = 'q0'  # Move back to rejection if invalid

    # Check for acceptance in final states q2 or q3
    if current_state in {'q2', 'q3'}:
        print("Accepted: The plural noun follows the correct rules.")
        return True
    else:
        print("Rejected: The plural noun does not follow the correct rules.")
        return False


# Run the FSA with user input
fsa_plural_noun()
