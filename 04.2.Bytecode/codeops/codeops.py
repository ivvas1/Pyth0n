import collections
import dis
import types
import typing as tp


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    ans: tp.Counter[str] = collections.Counter()
    for u in dis.get_instructions(source_code):
        ans[u.opname] += 1
        if isinstance(u.argval, types.CodeType):
            v = count_operations(u.argval)
            for j in v:
                ans[j] += v[j]
    return ans
