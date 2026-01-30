import pytest
from scraper_movie.random_string_generator import RandomStringGenerator


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