def max_list(lst: list[int]) -> int:
    n = len(lst)
    l = 0
    r = n - 1
    while r - l >= 3:
        m1 = l + (r - l) // 3
        m2 = r - (r - l) // 3
        if lst[m1] < lst[m2]:
            l = m1
        else:
            r = m2
    ans = lst[l]
    for i in range(l + 1, r + 1):
        ans = max(ans, lst[i])
    return ans
