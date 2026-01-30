import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scraper_movie')))

from scraper_movie.sum_calculator import SumCalculator


def test_empty_initialization():
    calc = SumCalculator()
    assert calc.calculate_sum() == 0


def test_single_number():
    calc = SumCalculator(5)
    assert calc.calculate_sum() == 5


def test_multiple_numbers():
    calc = SumCalculator(1, 2, 3)
    assert calc.calculate_sum() == 6


def test_invalid_type_raises_error():
    with pytest.raises(TypeError):
        SumCalculator(1, '2', 3)


def test_sum_of_integers():
    calc = SumCalculator(1, 2, 3, 4)
    assert calc.calculate_sum() == 10


def test_sum_of_floats():
    calc = SumCalculator(1.1, 2.2, 3.3)
    assert calc.calculate_sum() == 6.6


def test_sum_mixed_types():
    calc = SumCalculator(1, 2.5, 3)
    assert calc.calculate_sum() == 6.5


def test_sum_empty():
    calc = SumCalculator()
    assert calc.calculate_sum() == 0


def test_add_valid_number():
    calc = SumCalculator(1)
    calc.add_number(2)
    assert calc.calculate_sum() == 3


def test_add_invalid_number():
    calc = SumCalculator(1)
    with pytest.raises(TypeError):
        calc.add_number('a')


def test_clear_functionality():
    calc = SumCalculator(1, 2)
    calc.clear()
    assert calc.calculate_sum() == 0