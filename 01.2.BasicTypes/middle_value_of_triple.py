def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    if (b - a)*(c - a) <= 0:
        return a
    elif (a - b)*(c - b) <= 0:
        return b
    elif (b - c)*(a - c) <= 0:
        return c
