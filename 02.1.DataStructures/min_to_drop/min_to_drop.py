import typing as tp
from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    ans = len(seq)
    cnt = Counter(seq)
    for x in seq:
        ans = min(ans, len(seq) - cnt[x])
    return ans

