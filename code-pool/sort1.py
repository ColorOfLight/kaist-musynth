import random

myList = []
temp = range(500)
while c:
    n = random.randint(0, len(temp)-1)
    item = temp.pop(n)
    myList.append(item)

def swap(myList, nX, nY):
    temp = myList[nX]
    myList[nX] = myList[nY]
    myList[nY] = temp

def quickSort(myList, nStart, nEnd, level):
    nCount = nEnd - nStart    
    nMedianPoint = nEnd
    if nStart < nMedianPoint:
        nMedian = (nStart + nEnd) / 2
        swap(myList, nMedian, nEnd)
        nMedianPoint = nEnd
        nStartMove = nStart
        while nCount > 0 and nStartMove < nMedianPoint:
            nCount -= 1
            if myList[nStartMove] < myList[nMedianPoint]:
                swap(myList, nMedianPoint, nMedianPoint - 1)
                nMedianPoint -= 1                
                if nMedianPoint == nStartMove:
                    break                    
                else:
                    swap(myList, nStartMove, nMedianPoint + 1)
            else:
                nStartMove += 1

    if nStart < nMedianPoint - 1:
        quicksort(myList, nStart, nMedianPoint - 1, level+1)
    if nEnd > nMedianPoint + 1:
        quicksort(myList, nMedianPoint + 1, nEnd, level+1)

quickSort(myList, 0, len(myList)-1, 0)
print(b)