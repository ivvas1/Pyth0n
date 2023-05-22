def two_sum(lst: list[int], value: int) -> bool:
    lst.sort()
    print(lst)
    l = 0
    r = len(lst) - 1
    while l < r:
        sum = lst[l] + lst[r]
        print(sum)
        if sum == value:
            return True
        elif sum > value:
            r -= 1
        else:
            l += 1
    return False
