import hashlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from analysis import analysis


# Manipulation of shadow file

curr_dir = os.getcwd()              # Getting the currunt working directory
# locating and storing the path of shadow file to be read
file_path = os.path.join(curr_dir, 'shadow')
updated_user_dict = dict()
enc_list = ['md5', 'sha1', 'sha224', 'sha256',
            'sha384', 'sha512', 'sha3_224', 'sha3_256',
            'sha3_224', 'sha3_384', 'sha3_512']                                       # creating a list of encyrption techniques
# reading the file and storing its contents to the shadow_file variable
with open(file_path) as shadow_file:
    for i in shadow_file:
        # splitting the file into parts from first detection of ':' and stroing the contents in user and passwd
        user, passwd = i.split(':', 1)
        # creating the dictionary from the result above into user_dict, strip function removes any whitespaces and newline characters
        updated_user_dict[user] = passwd.strip()

user_dict = updated_user_dict.copy()

# Manipulation of dictionary file

orig_dict_list = []
# locating and storing the path of dictionary file to be read
cmn_dict_path = os.path.join(curr_dir, 'dictionary.txt')
with open(cmn_dict_path) as cmn_dict_file:
    for i in cmn_dict_file:
        # creating list for the data in dictionary file
        orig_dict_list.append(i.strip())

orig_list_len = len(orig_dict_list)


# decryption using over different algorithms
def decrypt(dict_list, method):
    # print(dict_list)
    start_time = time.time()
    temp_dict = user_dict.copy()
    
    global index
    for ind,i in enumerate(dict_list):    
        h = hashlib.new(method)
        temp = i 
        # creating a copy to manipulate the data
        # encoding the ascii to byte and then passing it to hash function
        h.update(temp.encode())
        # combinbing the hash without the whitespace and newline
        temp = h.hexdigest()
    
    
        for key, value in temp_dict.items():
            if temp == value:
                index = ind % orig_list_len
                updated_user_dict[key] = orig_dict_list[index]
                end_time = time.time()
                user_dict.pop(key)
                print(key)
                print(f"Elapsed time: {end_time - start_time:.2f} seconds")
                return updated_user_dict


# ceasar cipher


def ceasar_cipher(dict_list):
    print("ceasar")
    result = ""
    updated_list = []
    for j in range(1, 26):
        for i in dict_list:
            for char in i:
                if char.isalpha():
                    if char.isupper():
                        ascii_offset = 65
                    else:
                        ascii_offset = 97

                    # to find the shift
                    shifted_char = chr(
                        ((ord(char) - ascii_offset + j) % 26) + ascii_offset)
                    result += shifted_char

                else:
                    result += char
            updated_list.append(result)
            result = ""
    return updated_list


def leetspeak_decrypt(dict_list):
    # print("leetspeak")
    updated_list = []
    leetspeak_dict = {'a':'4', 'b': '8', 'e':'3', 'i': '!', 'l': '1', 'o':'0', 't':'7','s':'5', 'z':'2', 'g':'6' }
    
    for i in dict_list:
        word_list = list(i)
        for j,char in enumerate(word_list):
            if char in leetspeak_dict:
                # print(char, leetspeak_dict[char])
                word_list[j] = leetspeak_dict[char]
                
                        
        updated_word = ''.join(word_list)
        updated_list.append(updated_word)
    # print(updated_list)

    return updated_list


def salted_decryption(dict_list):
    print("salted")
    updated_list = []
    
    
    for w in dict_list:
        for i in range(0,1000000):
            salt = f'{i:05d}'
            salted_word = w + salt
            
            hashed_word = hashlib.md5(salted_word.encode()).hexdigest()  
            print(salted_word)
            
            for key,value in user_dict.items():
                if hashed_word == value:
                    updated_user_dict[key] = value
                    user_dict.pop(key)
                    return
        
def substitution_decrypt(dict_list):
    # print("substitution")
    updated_list = []
    desubstituted_dict = analysis()
    inverted_dict = {v: k for k, v in desubstituted_dict.items()}
    for l in dict_list:
        substituted_string = ""  # Initialize an empty string to store substituted characters
        for c in l:
            if c in inverted_dict:
                # If the character is in the mapping dictionary, substitute it
                substituted_string += inverted_dict[c]
            else:
                # If the character is not in the mapping dictionary, keep it unchanged
                substituted_string += c
        updated_list.append(substituted_string)  # Add the fully substituted string to the updated list
    return updated_list  # Return the fully updated list


if __name__ == "__main__":
    
    # decipher the ceasar, leet and salt
    user1 = decrypt(orig_dict_list, 'sha256')
    user3_list = ceasar_cipher(orig_dict_list)
    user3 = decrypt(user3_list, 'sha512')
    user4_list = leetspeak_decrypt(orig_dict_list)
    user4 = decrypt(user4_list,'sha1')
    user5 = decrypt(orig_dict_list, 'sha3_224')
    user6 = decrypt(orig_dict_list, 'sha224')
    user7_list = substitution_decrypt(orig_dict_list)
    user7 = decrypt(user7_list, 'sha3_512')
    user2 = salted_decryption(orig_dict_list)
    
    
 
    print(updated_user_dict)
