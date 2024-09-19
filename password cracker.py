import hashlib
import os
import itertools
import multiprocessing

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

temp_dict = updated_user_dict.copy()
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
def decrypt(dict_list):
    # print(dict_list)
    global index
    for ind,i in enumerate(dict_list):
        for j in enc_list:
            # creating a new hashlib function by iterating over the algorithms from list
            h = hashlib.new(j)
            temp = i 
            # creating a copy to manipulate the data
            # encoding the ascii to byte and then passing it to hash function
            h.update(temp.encode())
            # combinbing the hash without the whitespace and newline
            temp = h.hexdigest()
            
        # if needed we can update the algorithm that cracked the password

        # iterating over the dictionary, manipulating the data with cracked password
            for key, value in temp_dict.items():
                if len(user_dict) != 0:
                    if temp == value:
                        index = ind % orig_list_len
                        temp_dict[key] = orig_dict_list[index]
                        # updating the dictionary to remove the cracked user
                        user_dict.pop(key)
                else:
                    break
    return temp_dict

# ceasar cipher


def ceasar_cipher(dict_list):
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


def salted_decryption(dict_list, batch_size=10000000):
    batch = []
    # Using itertools.product to generate all combinations of length 5 from digits 0-9
    digits = '0123456789'
    possible_combinations = itertools.product(digits, repeat=5)
    pool = multiprocessing.Pool(multiprocessing.cpu_count()) 

    # Join the tuple to form a string and print
    comb = 0
    for combo in possible_combinations:
        all_digits = ''.join(combo)
        for i in dict_list:
            comb += 1
            batch.append(i + all_digits)
            if len(batch) >= batch_size:
                pool.apply_async(decrypt(batch), (batch,))
                print(comb)
                batch.clear()
    if batch:
        pool.apply_async(decrypt(batch), (batch,))
        # decrypt(batch)
    pool.close()  # Close the pool
    pool.join()
        
def substitution_decrypt(dict_list):
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


def decrypt_all():
    basic_dict = decrypt(orig_dict_list)
    ceasar_dict = decrypt(ceasar_cipher(orig_dict_list))
    leetspeak_dict = decrypt(leetspeak_decrypt(orig_dict_list))
    desubstituted_dec = decrypt(substitution_decrypt(orig_dict_list))
    salted_decryption(orig_dict_list)
    decrypted_dict = {**basic_dict, **ceasar_dict, **leetspeak_dict, **desubstituted_dec}
    return decrypted_dict

# updated_user_dict.update(decrypted_dict)
if __name__ == "__main__":
    
    decrypted_data = decrypt_all()
    # decipher the ceasar, leet and salt
            
    print(decrypted_data)
    print(user_dict)

