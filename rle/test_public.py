import copy
import dataclasses

import pytest
import testlib

from .rle import rle_multiply


@dataclasses.dataclass
class Case:
    list1: list[tuple[int, int]]
    list2: list[tuple[int, int]]
    result: any

    def __str__(self) -> str:
        return 'rle_{}_{}'.format(self.list1, self.list2)


TEST_CASES = [
    Case(list1=[(4, 1), (1, 2)], list2=[(2, 2), (3, 3)], result=16),
    Case(list1=[(4, 1), (2, 2)], list2=[(2, 2), (3, 3)], result=None),
    Case(list1=[(4, 1)], list2=[(2, 2), (3, 3)], result=None),
    Case(list1=[(5, 1), (1, 2), (4, 13), (1, 100), (3, 5)], list2=[(2, 2), (12, 3)], result=520),
    Case(list1=[(2, 1), (1, 2), (4, 13), (1, 100), (3, 5)], list2=[(2, 2), (13, 3)], result=None),
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_rle_multiply(t: Case) -> None:
    given_list1 = copy.deepcopy(t.list1)
    given_list2 = copy.deepcopy(t.list2)
    answer = rle_multiply(given_list1, given_list2)
    assert answer == t.result
