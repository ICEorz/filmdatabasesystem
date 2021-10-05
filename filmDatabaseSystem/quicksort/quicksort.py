def quick_sort(a, l, r, key=lambda t: t):
    if l >= r:
        return
    x = key(a[(l + r) // 2])
    i = l - 1
    j = r + 1
    while i < j:
        i += 1
        while key(a[i]) < x:
            i += 1
        j -= 1
        while key(a[j]) > x:
            j -= 1
        if i < j:
            a[i], a[j] = a[j], a[i]
    quick_sort(a, l, j, key)
    quick_sort(a, j + 1, r, key)

if __name__ == '__main__':
    s = [1, 3, 2, 6, 5, 4]
    quick_sort(s, 0, len(s) - 1)
    print(s)