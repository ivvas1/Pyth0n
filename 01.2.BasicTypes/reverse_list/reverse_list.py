def reverse_iterative(lst: list[int]) -> list[int]:
    """
    Return reversed list. You can use only iteration
    :param lst: input list
    :return: reversed list
    """
    ans = list()
    for i in range(len(lst) - 1, -1, -1):
        ans.append(lst[i])
    return ans


def reverse_inplace_iterative(lst: list[int]) -> None:
    """
    Revert list inplace. You can use only iteration
    :param lst: input list
    :return: None
    """
    n = len(lst)
    for i in range(n // 2):
        swap = lst[i]
        lst[i] = lst[n - i - 1]
        lst[n - i - 1] = swap


def reverse_inplace(lst: list[int]) -> None:
    """
    Revert list inplace with reverse method
    :param lst: input list
    :return: None
    """
    lst.reverse()


def reverse_reversed(lst: list[int]) -> list[int]:
    """
    Revert list with `reversed`
    :param lst: input list
    :return: reversed list
    """
    lst = list(reversed(lst))
    return lst


def reverse_slice(lst: list[int]) -> list[int]:
    """
    Revert list with slicing
    :param lst: input list
    :return: reversed list
    """
    return lst[len(lst) - 1:None:-1]
