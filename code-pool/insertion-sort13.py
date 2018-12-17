
def insertionSort(ar):
    x = len(ar)
    v = ar[x-1]
    j = x-2
    finarr = []
    while (ar[j] > v):
        j = j-1
    for k in range(0,j+1):
        finarr.append(ar[k])
    finarr.append(v)
    for k in range(j+2,x):
        finarr.append(ar[k-1])
    return finarr

n = int(input(''))
elem = input('')
numbers = elem.split()
	
arr = [] 
newarr = []
for i in range(0,n):
	arr.append(int(numbers[i])) 

newarr.append(arr[0])
for i in range(1,n):
	newarr.append(arr[i])
	newarr = insertionSort(newarr)

for i in range(0,n):
	print (newarr[i],end=" ")
print ("")
