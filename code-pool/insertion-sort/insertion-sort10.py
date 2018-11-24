def insertionSort2(ar):
    s = len(ar)-2
    check = int(ar[-1])
    for x in range(s,-1,-1):
        if int(ar[x]) <= check:
            ar[x+1] = str(check)
            break
        else:
            ar[x+1] = ar[x]
            if x == 0:
                ar[0] = str(check)
    return ar
s = input()
ar = input()
ar = ar.split()
for x in range(2,len(ar)+1):
    ar_check = insertionSort2(ar[:x])
    ar_rest = ar[x:]
    ar = ar_check + ar_rest
print(' ' .join(ar))