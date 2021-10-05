def get_next(a):
    i = 0
    j = -1
    nexti = [-1] * len(a)
    while i < len(a) - 1:
        if j == -1 or a[i] == a[j]:
            i += 1
            j += 1
            if i < len(a) and a[i] != a[j]:
                nexti[i] = j
            else:
                nexti[i] = nexti[j]
        else:
            j = nexti[j]
    return nexti


def kmp(s, p, nexti=None) -> bool:
    i = 0
    j = 0
    if not nexti:
        nexti = get_next(p)
    while i < len(s) and j < len(p):
        if j == -1 or s[i] == p[j]:
            i += 1
            j += 1
        else:
            j = nexti[j]
    if j == len(p):
        return True
    else:
        return False


if __name__ == '__main__':
    s = 'aabbccddaabb'
    p = 'ccdd'
    print(kmp(s, p))