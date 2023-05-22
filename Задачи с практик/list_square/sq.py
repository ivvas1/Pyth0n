def list_square(lst: list[int]) -> list[int]:
    n = len(lst)
    l = 0
    r = n - 1
    ans = list()
    while l <= r:
        if lst[l] ** 2 > lst[r] ** 2:
            ans.append(lst[l] ** 2)
            l += 1
        else:
            ans.append(lst[r] ** 2)
            r -= 1
    return list(reversed(ans))
