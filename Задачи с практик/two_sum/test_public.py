import copy
import dataclasses

import pytest
import testlib

from .two_sum import two_sum

@dataclasses.dataclass
class Case:
    lst: list[int]
    value: int
    result: bool

    def __str__(self) -> str:
        return 'sum_{}'.format(self.lst)


TEST_CASES = [
    Case(lst=[-5, 8, 3, 2, 0], value=2, result=True),
    Case(lst=[1, 8, 3, 2, 7], value=2, result=False),
    Case(lst=[-5, 8, 7, 7, 0], value=2, result=True),
    Case(lst=[-5, 8, 3, 2, 0, 90, 1, -6, 0], value=0, result=True),
    Case(lst=[], value=2, result=False)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_two_sum(t: Case) -> None:
    given_list = copy.deepcopy(t.lst)
    given_value = copy.deepcopy(t.value)
    answer = two_sum(given_list, given_value)
    assert answer == t.result
