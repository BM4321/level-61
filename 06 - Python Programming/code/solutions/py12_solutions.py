"""PY-12 reference solutions (searching and sorting). All sorts return NEW lists."""


def linear_search(xs: list, target) -> int:
    """Index of first occurrence or -1."""
    for i, x in enumerate(xs):
        if x == target:
            return i
    return -1


def binary_search(xs: list, target) -> int:
    """Iterative binary search on sorted xs (inclusive bounds); index or -1."""
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(xs: list, target) -> int:
    """Smallest i with xs[i] >= target (len(xs) if none); like bisect_left."""
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(xs: list, target) -> int:
    """Smallest i with xs[i] > target (len(xs) if none); like bisect_right."""
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo + hi) // 2
        if xs[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_occurrences(xs: list, target) -> int:
    """Occurrences of target in sorted xs in O(log n)."""
    return upper_bound(xs, target) - lower_bound(xs, target)


def selection_sort(xs: list) -> list:
    """Selection sort (not stable)."""
    a = xs[:]
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def insertion_sort(xs: list) -> list:
    """Stable insertion sort."""
    a = xs[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def bubble_sort(xs: list) -> list:
    """Bubble sort with early exit."""
    a = xs[:]
    n = len(a)
    for end in range(n - 1, 0, -1):
        swapped = False
        for j in range(end):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def merge(left: list, right: list) -> list:
    """Stable merge of two sorted lists."""
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def merge_sort(xs: list) -> list:
    """Top-down merge sort."""
    if len(xs) <= 1:
        return xs[:]
    mid = len(xs) // 2
    return merge(merge_sort(xs[:mid]), merge_sort(xs[mid:]))


def count_inversions(xs: list) -> int:
    """Number of pairs i < j with xs[i] > xs[j], in O(n log n)."""
    def sort_count(a: list) -> tuple[list, int]:
        if len(a) <= 1:
            return a[:], 0
        mid = len(a) // 2
        left, inv_l = sort_count(a[:mid])
        right, inv_r = sort_count(a[mid:])
        merged, i, j, inv = [], 0, 0, inv_l + inv_r
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                inv += len(left) - i
        merged += left[i:] + right[j:]
        return merged, inv

    return sort_count(xs)[1]


def insertion_sort_key_desc(xs: list, key=lambda x: x) -> list:
    """Stable descending insertion sort by key."""
    a = xs[:]
    for i in range(1, len(a)):
        item = a[i]
        j = i - 1
        while j >= 0 and key(a[j]) < key(item):
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = item
    return a
