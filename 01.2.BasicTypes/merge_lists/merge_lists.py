def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    if len(lst_b) == 0:
        return lst_a
    n = len(lst_a)
    m = len(lst_b)
    ans = list()
    i = 0
    j = 0
    while i < n and j < m:
        if lst_a[i] < lst_b[j]:
            ans.append(lst_a[i])
            i += 1

        else:
            ans.append(lst_b[j])
            j += 1

    while i < n:
        ans.append(lst_a[i])
        i += 1
    while j < m:
        ans.append(lst_b[j])
        j += 1
    return ans


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    return sorted(lst_a + lst_b)

