def rle_multiply(list1: list[tuple[int, int]], list2: list[tuple[int, int]]) -> any:
    n = len(list1)
    m = len(list2)
    len1, len2 = 0, 0
    for i in range(n):
        len1 += list1[i][0]
    for i in range(m):
        len2 += list2[i][0]
    if len1 != len2:
        return None
    ans = 0
    num1, num2, ind1, ind2 = 0, 0, 0, 0
    for i in range(len1):
        if ind1 == list1[num1][0]:
            num1 += 1
            ind1 = 0
        if ind2 == list2[num2][0]:
            num2 += 1
            ind2 = 0
        ans += list1[num1][1] * list2[num2][1]
        ind1 += 1
        ind2 += 1

    return ans


