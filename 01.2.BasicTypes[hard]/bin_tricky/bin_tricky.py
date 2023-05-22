import typing as tp


def find_median(nums1: tp.Sequence[int], nums2: tp.Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    m = len(nums1)
    n = len(nums2)

    if m == 0:
        if n % 2 == 0:
            return (nums2[n // 2] + nums2[(n - 1) // 2]) / 2
        return nums2[n // 2]
    elif n == 0:
        if m % 2 == 0:
            return (nums1[m // 2] + nums1[(m - 1) // 2]) / 2
        return nums1[m // 2]

    if m > n:
        n, m, nums1, nums2 = m, n, nums2, nums1

    li = 0
    ri = m
    mid = (m + n + 1) // 2

    while li <= ri:
        i = (li + ri) // 2
        j = mid - i

        if i > 0 and nums1[i - 1] > nums2[j]:
            ri = i - 1

        elif i < m and nums1[i] < nums2[j - 1]:
            li = i + 1

        else:
            l = 0
            r = 0
            if i == 0:
                l = nums2[j - 1]
            elif j == 0:
                l = nums1[i - 1]
            else:
                l = max(nums2[j - 1], nums1[i - 1])

            if i == m:
                r = nums2[j]
            elif j == n:
                r = nums1[i]
            else:
                r = min(nums1[i], nums2[j])

            if (m + n) % 2 == 1:
                return float(l)
            return float((l + r) / 2)



