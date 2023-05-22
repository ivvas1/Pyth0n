import typing as tp


def filter_list_by_list(lst_a: tp.Union[list[int], range], lst_b: tp.Union[list[int], range]) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    n = len(lst_a)
    m = len(lst_b)
    ans = list()
    i = 0
    j = 0
    while i < n:
        while j < m and lst_a[i] > lst_b[j]:
            j += 1
        if j == m or lst_a[i] != lst_b[j]:
            ans.append(lst_a[i])
        i += 1
    return ans
