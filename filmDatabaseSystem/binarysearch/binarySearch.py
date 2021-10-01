def lower_bound(flist, x, l=0, r=None, key=lambda t: t):
    if r is None:
        r = len(flist)
    while l < r:
        mid = (l + r) // 2
        if key(flist[mid]) >= x:
            r = mid
        else:
            l = mid + 1
    return l


def upper_bound(flist, x, l=0, r=None, key=lambda t: t):
    if r is None:
        r = len(flist)
    while l < r:
        mid = (l + r) // 2
        if key(flist[mid]) > x:
            r = mid
        else:
            l = mid + 1
    return l


if __name__ == '__main__':
    a = range(29)

    print(lower_bound(a, 0, len(a) - 1, 16))
    print(upper_bound(a, 0, len(a) - 1, 30))