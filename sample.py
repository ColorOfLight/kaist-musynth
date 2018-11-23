def insertionSort(x):
    for size in range(1, len(x)):
        val = x[size]
        # i = size
        __HOLE__ = None
        while i > 0 and x[i-1] > val:
            x[i] = x[i-1]
            i -= 1
        x[i] = val

insertionSort([1,2])
