import hashlib
import os
import time
from analysis import analysis

# Manipulation of shadow file to extract usernames and hashed passwords
curr_dir = os.getcwd()  # Get the current working directory
file_path = os.path.join(curr_dir, 'shadow')  # Locate the shadow file containing usernames and password hashes

# Initialize a dictionary to store usernames and their corresponding hashed passwords
updated_user_dict = dict()

# Reading the shadow file line by line and extracting the usernames and password hashes
with open(file_path) as shadow_file:
    for i in shadow_file:
        # Split each line at the first occurrence of ':' to separate the username and hashed password
        user, passwd = i.split(':', 1)
        # Add the username and cleaned hashed password to the dictionary
        updated_user_dict[user] = passwd.strip()

# Make a copy of the shadow file dictionary for manipulation during decryption
user_dict = updated_user_dict.copy()

# Manipulation of dictionary file to create a list of potential passwords
orig_dict_list = []  # Initialize a list to hold words from the dictionary file
cmn_dict_path = os.path.join(curr_dir, 'dictionary.txt')  # Locate the dictionary file

# Read the dictionary file and store each line (word) as an element in the list
with open(cmn_dict_path) as cmn_dict_file:
    for i in cmn_dict_file:
        orig_dict_list.append(i.strip())  # Strip newline characters and add the word to the list

orig_list_len = len(orig_dict_list)  # Store the length of the original dictionary list

# Function to decrypt passwords using different hashing algorithms
def decrypt(dict_list, method):
    start_time = time.time()  # Start timing the decryption process
    temp_dict = user_dict.copy()  # Create a copy of user_dict to avoid modifying the original during iteration
    
    global index  # Define a global index variable to track decrypted entries
    for ind, i in enumerate(dict_list):
        h = hashlib.new(method)  # Initialize a new hashing object with the specified algorithm
        temp = i  # Copy the current word for hashing
        h.update(temp.encode())  # Encode the word to bytes and hash it
        temp = h.hexdigest()  # Convert the hash to a hexadecimal string
    
        # Check if the computed hash matches any user password hash in temp_dict
        for key, value in temp_dict.items():
            if temp == value:
                index = ind % orig_list_len  # Find the index of the original word in the dictionary
                updated_user_dict[key] = orig_dict_list[index]  # Update the user dictionary with the decrypted password
                end_time = time.time()  # End timing
                user_dict.pop(key)  # Remove the decrypted user from the original user_dict
                print(key)  # Print the username that was decrypted
                print(f"Elapsed time: {end_time - start_time:.2f} seconds")  # Print the time taken to decrypt
                return updated_user_dict  # Return the updated dictionary

# Function to apply Caesar cipher shifts to each word in the dictionary list
def ceasar_cipher(dict_list):
    print("ceasar")  # Print cipher type being used
    result = ""  # Initialize an empty string to store the shifted characters
    updated_list = []  # List to hold all shifted versions of each word
    
    # Iterate through all possible shifts (1 to 25)
    for j in range(1, 26):
        # Iterate through each word in the dictionary list
        for i in dict_list:
            for char in i:
                if char.isalpha():  # Check if the character is alphabetic
                    # Determine the ASCII offset based on whether the character is upper or lower case
                    ascii_offset = 65 if char.isupper() else 97

                    # Calculate the shifted character and append to the result string
                    shifted_char = chr(((ord(char) - ascii_offset + j) % 26) + ascii_offset)
                    result += shifted_char
                else:
                    result += char  # Keep non-alphabetic characters unchanged
            updated_list.append(result)  # Add the shifted word to the updated list
            result = ""  # Reset the result for the next word
    return updated_list  # Return the list of all shifted words

# Function to decrypt words using leet speak substitutions
def leetspeak_decrypt(dict_list):
    updated_list = []  # List to hold leet speak variations of words
    # Dictionary defining leet speak substitutions
    leetspeak_dict = {'a': '4', 'b': '8', 'e': '3', 'i': '!', 'l': '1', 'o': '0', 't': '7', 's': '5', 'z': '2', 'g': '6'}
    
    # Iterate through each word in the dictionary list
    for i in dict_list:
        word_list = list(i)  # Convert the word to a list of characters
        for j, char in enumerate(word_list):
            if char in leetspeak_dict:  # Check if the character has a leet substitution
                word_list[j] = leetspeak_dict[char]  # Substitute the character with its leet equivalent
                
        updated_word = ''.join(word_list)  # Reconstruct the word from the substituted characters
        updated_list.append(updated_word)  # Add the substituted word to the list
    return updated_list  # Return the updated list of leet speak words

# Function to decrypt passwords that are salted using a 5-digit salt
def salted_decryption(dict_list):
    print("salted")  # Print the decryption type being used
    updated_list = []  # Initialize an empty list for future use (if needed)
    
    # Iterate through each word in the dictionary list
    for w in dict_list:
        # Try each 5-digit salt (00000 to 99999)
        for i in range(0, 1000000):
            salt = f'{i:05d}'  # Format the current number as a 5-digit string
            salted_word = w + salt  # Append the salt to the word
            
            # Hash the salted word using MD5
            hashed_word = hashlib.md5(salted_word.encode()).hexdigest()
            print(salted_word)  # Print the current salted word being hashed
            
            # Check if the hash matches any stored hash in the user dictionary
            for key, value in user_dict.items():
                if hashed_word == value:
                    updated_user_dict[key] = value  # Update the decrypted password for the user
                    user_dict.pop(key)  # Remove the user from the original dictionary
                    return

# Function to decrypt passwords using character substitution analysis
def substitution_decrypt(dict_list):
    updated_list = []  # List to hold substituted variations of words
    desubstituted_dict = analysis()  # Get the character substitution mapping dictionary from the analysis function
    inverted_dict = {v: k for k, v in desubstituted_dict.items()}  # Invert the mapping dictionary for substitution
    
    # Iterate through each word in the dictionary list
    for l in dict_list:
        substituted_string = ""  # Initialize an empty string to store substituted characters
        for c in l:
            if c in inverted_dict:  # If the character is in the inverted mapping dictionary, substitute it
                substituted_string += inverted_dict[c]
            else:
                substituted_string += c  # If not in the dictionary, keep the character unchanged
        updated_list.append(substituted_string)  # Add the fully substituted string to the updated list
    return updated_list  # Return the list of substituted words

# Main execution block
if __name__ == "__main__":
    
    # Decrypt passwords using various approaches based on knowledge of cipher types and salts
    user1 = decrypt(orig_dict_list, 'sha256')  # Decrypt using SHA-256
    user3_list = ceasar_cipher(orig_dict_list)  # Apply Caesar cipher shifts to the dictionary
    user3 = decrypt(user3_list, 'sha512')  # Decrypt shifted words using SHA-512
    user4_list = leetspeak_decrypt(orig_dict_list)  # Apply leet speak substitutions to the dictionary
    user4 = decrypt(user4_list, 'sha1')  # Decrypt leet speak words using SHA-1
    user5 = decrypt(orig_dict_list, 'sha3_224')  # Decrypt using SHA3-224
    user6 = decrypt(orig_dict_list, 'sha224')  # Decrypt using SHA-224
    user7_list = substitution_decrypt(orig_dict_list)  # Apply substitution analysis to the dictionary
    user7 = decrypt(user7_list, 'sha3_512')  # Decrypt substituted words using SHA3-512
    user2 = salted_decryption(orig_dict_list)  # Decrypt salted words using MD5
    
    # Print the final updated dictionary containing decrypted passwords for each user
    print(updated_user_dict)
