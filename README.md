# Homework 1 - Network Security (CS 468)

## Overview

This project focuses on breaking ciphers and authentication systems. It consists of two tasks: performing an offline dictionary attack to crack passwords and breaking a substitution cipher. The code is implemented in Python 3.5 or later.

## Tasks

### Task 1: Password Cracking With Dictionary Attacks

The goal of this task is to crack passwords stored in a simplified version of the Linux `/etc/shadow` file using an offline dictionary attack. The passwords have been hashed using different hashing algorithms such as MD5, SHA1, and SHA256, and some include additional security measures such as salts, Caesar cipher encoding, and leet speak transformations.

#### Key Features:
- Cracks passwords of users `user1` through `user6`.
- Handles salted hashes, encoded passwords, and passwords with leet transformations.
- Uses a custom Python script to automate the cracking process.

### Task 2: Breaking Substitution Ciphers

In this task, the objective is to crack the password of `user7`, who uses a substitution cipher before hashing the password. Additionally, the task involves decrypting a text file using the same substitution cipher.

#### Key Features:
- Analyzes encrypted text to identify the substitution cipher mapping.
- Applies the discovered mapping to crack the password.
- Decrypts and retrieves the plaintext of the encrypted document.

## Files

- `password_cracker.py`: Main script for Task 1 that performs the dictionary attack.
- `passwords.txt`: Contains usernames and their cracked passwords in the format `user:password`.
- `explanation_1.txt`: Describes the approach, execution time, and challenges faced during Task 1.
- `analysis.py`: Script for Task 2 to analyze the substitution cipher and crack the password for `user7`.
- `plaintext.txt`: The decrypted text from the encrypted document in Task 2.
- `explanation.txt`:  Describes the approach, execution time, and challenges faced during Task 1 and explanation of the approach used in Task 2, including any resources used.
