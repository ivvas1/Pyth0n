import copy
import dataclasses

import pytest
import testlib

from .levin import levin


@dataclasses.dataclass
class Case:
    s1: str
    s2: str
    result: bool

    def __str__(self) -> str:
        return 'dist_{}_{}'.format(self.s1, self.s2)


TEST_CASES = [
    Case(s1="", s2="", result=True),
    Case(s1="", s2="x", result=True),
    Case(s1="", s2="ab", result=False),
    Case(s1="ax", s2="c", result=False),
    Case(s1="AVchdks", s2="AVhdks", result=True)
]


@pytest.mark.parametrize('t', TEST_CASES, ids=str)
def test_levin(t: Case) -> None:
    given_s1 = copy.deepcopy(t.s1)
    given_s2 = copy.deepcopy(t.s2)
    answer = levin(given_s1, given_s2)
    assert answer == t.result
