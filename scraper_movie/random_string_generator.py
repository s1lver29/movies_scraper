import random
import string

class RandomStringGenerator:
    @staticmethod
    def generate_random_string(length: int) -> str:
        if length < 1 or length > 20:
            raise ValueError('Length must be between 1 and 20')
        letters = string.ascii_letters  # a-z, A-Z
        return ''.join(random.choice(letters) for _ in range(length))