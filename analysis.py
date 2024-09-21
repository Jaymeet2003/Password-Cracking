import os
import hashlib
import itertools

# Open the 'encrypted.txt' file and read its content as cipher text
with open('encrypted.txt', 'r') as file:
    cipher_text = file.read()

# Print the cipher text to check its contents
print(cipher_text)

# Expected frequency order of English letters from most to least common
english_freq_order = 'ETAHNOISDLRFGCMUWBPYVKQXJZ'

# Convert the frequency order to lowercase for easy mapping
english_freq_order_lower = english_freq_order.lower()

# Initialize a dictionary to hold frequency counts of each character in the cipher text
frequency = dict()

# Count the frequency of each character in the cipher text
for char in cipher_text:
    if char in frequency:
        frequency[char] += 1  # Increment count if character is already in the dictionary
    else:
        frequency[char] = 1   # Initialize count if character is not in the dictionary

# Sort the frequency dictionary in descending order by the frequency of characters
frequency_sorted = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

# Initialize a dictionary to map cipher characters to their corresponding English letters
mapping_dict = dict()

# Filter out non-alphabetic characters like spaces, punctuation from the frequency count
filtered_frequency = {key: val for key, val in frequency_sorted.items() if not any(char in key for char in [' ', ',', '.', ';'])}

# Map the most frequent cipher text characters to the most frequent English letters
for cipher_char, _ in filtered_frequency.items():
    if len(mapping_dict) < len(english_freq_order_lower):
        # Map the current cipher character to the corresponding English letter based on frequency order
        mapping_dict[cipher_char] = english_freq_order_lower[len(mapping_dict)]

# Function to return the mapping dictionary
def analysis():
    return mapping_dict

# Initialize a string to hold the text after applying the character substitution based on frequency analysis
desubstituted_text = ''

# Substitute each character in the cipher text using the frequency mapping
for l in cipher_text:
    if l in mapping_dict:
        desubstituted_text += mapping_dict[l]  # Substitute character if it exists in the mapping
    else:
        desubstituted_text += l  # Leave the character as is if it doesn't exist in the mapping

# Print the desubstituted text to see the partially decrypted message
print(desubstituted_text)
