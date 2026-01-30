def _validate_inputs(self, numbers):
        for number in numbers:
            if not isinstance(number, (int, float)):
                raise TypeError(f'Expected int or float, got {type(number).__name__}')
def __init__(self, *numbers):
        self._validate_inputs(numbers)
        self.numbers = numbers

    def calculate_sum(self) -> float:
        """
        Calculate the sum of all numbers.
        
        Returns:
            Sum of all numbers. Returns 0 if no numbers provided.
            
        Examples:
            >>> calc = SumCalculator(1, 2, 3)
            >>> calc.calculate_sum()
            6
        """def total(self) -> float:
        warnings.warn("total() is deprecated, use calculate_sum() instead", DeprecationWarning)
        return self.calculate_sum()