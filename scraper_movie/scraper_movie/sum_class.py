def _validate_inputs(self, numbers):
        for number in numbers:
            if not isinstance(number, (int, float)):
                raise TypeError(f'Expected int or float, got {type(number).__name__}')