import os
import hashlib
import itertools


with open('encrypted.txt', 'r') as file:
    cipher_text = file.read()
print(cipher_text)
    

# english_freq_order = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

english_freq_order = 'ETAHNOISDLRFGCMUWBPYVKQXJZ'


english_freq_order_lower = english_freq_order.lower()

frequency = dict()

for char in cipher_text:
    if char in frequency:
        frequency[char] += 1        
    else:
        frequency[char] = 1
            
frequency_sorted = dict(sorted(frequency.items(), key=lambda item: item[1], reverse=True))

mapping_dict = dict()

filtered_frequency = {key: val for key, val in frequency_sorted.items() if not any(char in key for char in [' ', ',', '.', ';'])}

for cipher_char, _ in filtered_frequency.items():
    if len(mapping_dict) < len(english_freq_order_lower):
        mapping_dict[cipher_char] = english_freq_order_lower[len(mapping_dict)]
        
# print(mapping_dict)

def analysis():
    return mapping_dict



desubstituted_text = ''

for l in cipher_text:
    if l in mapping_dict:
        desubstituted_text += mapping_dict[l]
    else:
        desubstituted_text += l
        
# print(desubstituted_text)
        
        

