from typing import Union, Tuple

class SumCalculator:
    def __init__(self, *numbers: Union[int, float]) -> None:
        if numbers:
            self.add_numbers(numbers)
        self.validate_numbers()
        self.validate_numbers()
        self._numbers = []
        self.validate_numbers()
        if numbers:
            self.add_numbers(numbers)

    def add_numbers(self, numbers: Tuple[Union[int, float], ...]) -> None:
        for number in numbers:
            self.add_number(number)

    def calculate_sum(self) -> Union[int, float]:
        return sum(self.numbers) if self.numbers else 0

    def add_number(self, number: Union[int, float]) -> None:
        if not isinstance(number, (int, float)):
            raise TypeError(f"Expected int or float, got {type(number).__name__}")
        self._numbers.append(number)
        if not isinstance(number, (int, float)):
            raise TypeError(f"Expected int or float, got {type(number).__name__}")
        # The above line is redundant due to the add_number function adding numbers to self._numbers

    def clear(self) -> None:
        self.numbers = []

    @property
    def numbers(self) -> Tuple[Union[int, float], ...]:
        return tuple(self._numbers)

    def __str__(self) -> str:
        return f'SumCalculator({self.numbers})'

    def __repr__(self) -> str:
        return f'SumCalculator(numbers={self.numbers})'def validate_numbers(self) -> None:
        if not self._numbers:
            return
        for number in self._numbers:
            if not isinstance(number, (int, float)):
                raise TypeError(f"Expected int or float, but got {type(number).__name__}")