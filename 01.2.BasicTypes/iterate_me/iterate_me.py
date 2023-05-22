import typing as tp


def get_squares(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with squared values
    """
    ans = list()
    for i in elements:
        ans.append(i ** 2)
    return ans

# ====================================================================================================


def get_indices_from_one(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with indices started from 1
    """
    n = len(elements)
    ans = list()
    for i in range(n):
        ans.append(i + 1)
    return ans


# ====================================================================================================


def get_max_element_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of maximum element if exists, None otherwise
    """
    n = len(elements)
    if n == 0:
        return None
    ans = elements[0]
    ind = 0
    for i in range(n):
        if elements[i] > ans:
            ind = i
            ans = elements[i]
    return ind


# ====================================================================================================


def get_every_second_element(elements: list[int]) -> list[int]:
    """
    :param elements: list with integer values
    :return: list with each second element of list
    """
    ans = list()
    for i in range(1, len(elements), 2):
        ans.append(elements[i])
    return ans

# ====================================================================================================


def get_first_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of first "3" in the list if exists, None otherwise
    """
    for i in range(len(elements)):
        if elements[i] == 3:
            return i

    return None


# ====================================================================================================


def get_last_three_index(elements: list[int]) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :return: index of last "3" in the list if exists, None otherwise
    """
    for i in range(len(elements) - 1, -1, -1):
        if elements[i] == 3:
            return i

    return None

# ====================================================================================================


def get_sum(elements: list[int]) -> int:
    """
    :param elements: list with integer values
    :return: sum of elements
    """
    return sum(elements)


# ====================================================================================================


def get_min_max(elements: list[int], default: tp.Optional[int]) -> tuple[tp.Optional[int], tp.Optional[int]]:
    """
    :param elements: list with integer values
    :param default: default value to return if elements are empty
    :return: (min, max) of list elements or (default, default) if elements are empty
    """
    ans = (default, default)
    if len(elements) == 0:
        return ans
    mn = elements[0]
    mx = elements[0]
    for i in elements:
        mn = min(i, mn)
        mx = max(i, mx)
    ans = (mn, mx)
    return ans



# ====================================================================================================


def get_by_index(elements: list[int], i: int, boundary: int) -> tp.Optional[int]:
    """
    :param elements: list with integer values
    :param i: index of elements to check with boundary
    :param boundary: boundary for check element value
    :return: element at index `i` from `elements` if element greater then boundary and None otherwise
    """
    return ans if (ans := elements[i]) > boundary else None

