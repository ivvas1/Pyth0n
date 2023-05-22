import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    ans = []
    for a in seq:
        for x in a:
            heapq.heappush(ans, x)
            ans.sort()
    return ans
