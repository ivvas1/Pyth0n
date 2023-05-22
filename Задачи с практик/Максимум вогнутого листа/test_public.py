import copy
import dataclasses

import pytest
import testlib

from .max_list import max_list


@dataclasses.dataclass
class Case:
    lst: list[int]
    result: int

    def __str__(self) -> str:
        return 'max_{}'.format(self.lst)


TEST_CASES = [
    Case(lst=[1, 3, 4, 7, 9, 6, -1, -3], result=9),
    Case(lst=[0], result=0),
    Case(lst=[1, 10, 1], result=10),
    Case(lst=[1, 3, 4, 7, 6, 6, -1, -3], result=7),
    Case(lst=[1, 2], result=2)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_max_list(t: Case) -> None:
    given_list = copy.deepcopy(t.lst)
    answer = max_list(given_list)
    assert answer == t.result
