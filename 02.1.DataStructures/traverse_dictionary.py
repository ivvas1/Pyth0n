import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    ans = list()
    for elem in dct.keys():
        if type(dct[elem]) == dict:
            if prefix != "":
                ans += traverse_dictionary_immutable(dct[elem], prefix + "." + elem)
            else:
                ans += traverse_dictionary_immutable(dct[elem], elem)

        else:
           if prefix != "":
                ans.append((prefix + "." + elem, dct[elem]))
           else:
               ans.append((elem, dct[elem]))

    return ans


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    for elem in dct.keys():
        if type(dct[elem]) == dict:
            if prefix != "":
                traverse_dictionary_mutable(dct[elem], result, prefix + "." + elem)
            else:
                traverse_dictionary_mutable(dct[elem], result, elem)

        else:
            if prefix != "":
                result.append((prefix + "." + elem, dct[elem]))
            else:
                result.append((elem, dct[elem]))


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
        ) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    q = []
    q.append((dct, ""))
    ans = list()
    while q:
        elem = q.pop()
        p = elem[1]
        for i in elem[0].keys():
            if type(elem[0][i]) == dict:
                if p == "":
                    q.append((elem[0][i], i))
                else:
                    q.append((elem[0][i], p + "." + i))
            else:
                if p == "":
                    ans.append((i, elem[0][i]))
                else:
                    ans.append((p + "." + i, elem[0][i]))

    return ans


