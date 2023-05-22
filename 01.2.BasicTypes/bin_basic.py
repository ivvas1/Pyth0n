import typing as tp


def find_value(nums: tp.Union[list[int], range], value: int) -> bool:

    """

    Find value in sorted sequence

    :param nums: sequence of integers. Could be empty

    :param value: integer to find

    :return: True if value exists, False otherwise

    """

    l = -1

    r = len(nums)

    while l + 1 < r:

        mid = (l + r) // 2

        if nums[mid] == value:

            return True

        elif nums[mid] <= value:

            l = mid

        else:

            r = mid

    return False

