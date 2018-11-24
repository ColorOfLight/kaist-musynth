def insert(ar, index):
    while index>0:
        if ar[index-1]>ar[index] :
            tmp = ar[index]
            ar[index] = ar[index-1]
            ar[index-1] = tmp
            index = index-1
        else:
            return ar
    return ar
def insertionSort(ar):
    for i in range(len(ar)-1):
        ar = insert(ar, i+1)
                 
num = [int(i) for i in input().strip().split()]
ar = [int(j) for j in input().strip().split()]
insertionSort(ar)
print(*ar)