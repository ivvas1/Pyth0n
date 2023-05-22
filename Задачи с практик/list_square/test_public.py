import copy
import dataclasses

import pytest
import testlib

from .sq import list_square


@dataclasses.dataclass
class Case:
    lst: list[int]
    result: list[int]

    def __str__(self) -> str:
        return 'sort_{}'.format(self.lst)


TEST_CASES = [
    Case(lst=[], result=[]),
    Case(lst=[1, 2, 3], result=[1, 4, 9]),
    Case(lst=[15], result=[225]),
    Case(lst=[-1, 2, 3], result=[1, 4, 9]),
    Case(lst=[-2, -1, 2, 3], result=[1, 4, 4, 9]),
    Case(lst=[-4, -2, -1, 2, 3], result=[1, 4, 4, 9, 16])
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_list_square(t: Case) -> None:
    given_list = copy.deepcopy(t.lst)
    answer = list_square(given_list)
    assert answer == t.result
