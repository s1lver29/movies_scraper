import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from scraper_movie.scraper_movie.sum_calculator import SumCalculator


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
        SumCalculator(1, 2, 'three') 


def test_add_valid_number():
    calc = SumCalculator(1)
    calc.add_number(2)
    assert calc.calculate_sum() == 3


def test_add_invalid_number():
    calc = SumCalculator(1)
    with pytest.raises(TypeError):
        calc.add_number('two')


def test_clear_functionality():
    calc = SumCalculator(1, 2, 3)
    calc.clear()
    assert calc.calculate_sum() == 0


def test_large_numbers():
    calc = SumCalculator(1e18, 1e18)
    assert calc.calculate_sum() == 2e18


def test_float_precision():
    calc = SumCalculator(0.1, 0.2)
    assert calc.calculate_sum() == pytest.approx(0.3)