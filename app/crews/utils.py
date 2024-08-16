def divide_by_zero_handler(numerator: float, denominator: float, default=0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator
