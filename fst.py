def fst_pluralize():
    """
    FST that pluralizes English words based on the e-insertion rule.
    Accepts user input for a word in lexical form with morpheme and word boundaries.

    Example input: "fox^s#"

    Returns:
    - str: The plural form of the word.
    """
    # Define characters that require "e" insertion before "s#"
    insertion_required = {'x', 's', 'z'}

    # Initialize the FST to start state
    state = "q1"

    # Get user input
    try:
        word = input("Enter the lexical form of the word (e.g., 'fox^s#'): ").strip().lower()
    except EOFError:
        print("Error: No input detected.")
        return None

    # Process input through states
    while True:
        if state == "q1":  # Initial state: validate input format
            if "^s#" in word and word.endswith("s#"):
                state = "q2"
            else:
                print("Error: Input format is incorrect. Make sure to use '^s#' after the word.")
                return None

        elif state == "q2":  # Split input at morpheme boundary
            base_word, suffix = word.split("^")
            state = "q3"

        elif state == "q3":  # Determine if "e" insertion is needed
            last_char = base_word[-1]
            if last_char in insertion_required:
                state = "q4"  # "e" insertion required
            else:
                state = "q5"  # No "e" insertion needed

        elif state == "q4":  # Add "es" for words ending in x, s, z
            plural_form = base_word + "es"
            state = "q6"

        elif state == "q5":  # Add "s" for other words
            plural_form = base_word + "s"
            state = "q6"

        elif state == "q6":  # Final state: Output the plural form
            print("Plural form:", plural_form)
            return plural_form

# Explicitly call the function to ensure it runs and prompts for input
fst_pluralize()
