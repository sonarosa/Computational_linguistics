def levenshtein_distance_custom(str1, str2):
    # Initialize the matrix for DP
    len1, len2 = len(str1), len(str2)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Fill in base cases for empty strings
    for i in range(len1 + 1):
        dp[i][0] = i  # Cost of deleting all characters
    for j in range(len2 + 1):
        dp[0][j] = j  # Cost of inserting all characters

    # Fill in the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No cost for identical substitution
            else:
                # Minimum of insert, delete, or substitute with cost considerations
                dp[i][j] = min(dp[i][j - 1] + 1,      # Insert
                               dp[i - 1][j] + 1,      # Delete
                               dp[i - 1][j - 1] + 2)  # Substitute with cost 2

    # Reconstruct the edit operations
    operations = []
    i, j = len1, len2
    while i > 0 or j > 0:
        if i > 0 and j > 0 and str1[i - 1] == str2[j - 1]:
            i, j = i - 1, j - 1  # Move diagonally, no operation needed
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            operations.append(f"Insert '{str2[j - 1]}' at position {i}")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            operations.append(f"Delete '{str1[i - 1]}' from position {i - 1}")
            i -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 2:
            operations.append(f"Replace '{str1[i - 1]}' with '{str2[j - 1]}' at position {i - 1}")
            i, j = i - 1, j - 1

    # Return the customized Levenshtein distance and the operations
    return dp[len1][len2], operations[::-1]

# Example usage
str1 = "intention"
str2 = "execution"
distance, operations = levenshtein_distance_custom(str1, str2)
print("Custom Levenshtein Distance:", distance)
print("Edit Operations:")
for op in operations:
    print(op)
