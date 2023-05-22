def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    if type1 == str or type2 == str:
        return str
    elif type1 == list or type2 == list:
        if type2 == list:
            type1, type2 = type2, type1
        if type2 != range and type2 != list and type2 != tuple:
            return str
        return list
    elif type1 == tuple or type2 == tuple:
        if type2 == tuple:
            type1, type2 = type2, type1
        if type2 == range or type2 == tuple:
            return tuple
        return str
    elif type1 == range or type2 == range:
        if type2 == range:
            type1, type2 = type2, type1
        if type2 == range:
            return tuple
        return str
    elif type1 == bool or type2 == bool:
        if type2 == bool:
            type1, type2 = type2, type1
        if type2 == bool:
            return bool
        elif type2 == int:
            return int
        elif type2 == float:
            return float
        elif type2 == complex:
            return complex
    elif type1 == float or type2 == float:
        if type2 == float:
            type1, type2 = type2, type1
        if type2 == complex:
            return complex
        return float
    elif type1 == int or type2 == int:
        if type2 == int:
            type1, type2 = type2, type1
        if type2 == int:
            return int
        return complex
    return complex


