from string import ascii_letters, digits
from random import randint


def generate_key():
    allowed_characters = list(digits) + list(ascii_letters)
    size_key = randint(100, 500)
    size_allowed_characters = len(allowed_characters)
    
    key = ''
    for i in range(size_key):
        letter = allowed_characters[randint(0, size_allowed_characters-1)]
        key += letter

    return key

