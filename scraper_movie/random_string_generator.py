import random
import string

class RandomStringGenerator:
    @staticmethod
    def generate_random_string(length: int) -> str:
        if length < 1 or length > 20:
            raise ValueError('Length must be between 1 and 20')
        letters = string.ascii_letters  # a-z, A-Z
        return ''.join(random.choice(letters) for _ in range(length))# Unit tests for RandomStringGenerator
# Unit tests for RandomStringGenerator
import pytest
import pytest


def test_generate_random_string_length():
    result = RandomStringGenerator.generate_random_string(10)
    assert len(result) == 10


def test_generate_random_string_min_length():
    result = RandomStringGenerator.generate_random_string(1)
    assert len(result) == 1


def test_generate_random_string_max_length():
    result = RandomStringGenerator.generate_random_string(20)
    assert len(result) == 20


def test_generate_random_string_invalid_length():
    with pytest.raises(ValueError):
        RandomStringGenerator.generate_random_string(0)
    with pytest.raises(ValueError):
        RandomStringGenerator.generate_random_string(21)