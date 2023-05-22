def levin(s1: str, s2: str) -> bool:
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    n = len(s1)
    m = len(s2)
    if n >= m + 2:
        return False
    i = 0
    j = 0
    if n == m + 1:
        while j < m and s1[i] == s2[j]:
            i += 1
            j += 1
        if j == m:
            return True
        i += 1
        while j < m and s1[i] == s2[j]:
            i += 1
            j += 1
        if j == m:
            return True
        return False
    else:
        while j < m and s1[i] == s2[j]:
            i += 1
            j += 1
        if j == m:
            return True
        return False
