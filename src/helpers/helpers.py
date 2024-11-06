import random
import string


def generate_token():
    first_char = random.choice(string.ascii_letters)
    rest = ''.join(random.choices(string.ascii_letters + string.digits, k=19))

    return first_char + rest
