import random
import string

plaintext_flag = "AAAA"


def encrypt_flag(plain_flag):
    letters = string.ascii_letters
    encrypted_flag = ""
    for char in plain_flag:
        random_letter_for_confusion = random.choice(letters)
        chars_to_add = chr(ord(char) + 1) + random_letter_for_confusion
        encrypted_flag += chars_to_add

    return encrypted_flag


print(encrypt_flag(plaintext_flag))
