import typing as tp
import collections

def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    ans = dict()
    print(ans)
    for x in dct.keys():
        ans[dct[x]] = ans.get(dct[x], []) + [x]
    return ans
