# Answer : 	
# if arr[1] < arr[0]:
#	arr = [arr[1], arr[0]]
# Function : Append an element into a list.

def insertionSort1(arr):
	length = len(arr)
	v = arr[length-1]
	if length == 2:
		__HOLE__ = None
		return arr

	for i in range(length-2,-1,-1):
		if arr[i] > v:
			arr[i+1] = arr[i]
		else:
			arr[i+1] = v
			break

	if arr[0] > v:
		arr[0] = v
	return arr

def insertionSort(arr):
	length = len(arr)
	for i in range(1,length):
		if arr[i] < arr[i-1]:
			arr[:i+1] = insertionSort1(arr[:i+1])
		temp = arr
		
length = int(input())
temp = input().strip().split()
arr = []
for i in range(0,len(temp)):
    arr.append(int(temp[i]))
insertionSort(arr)

s=""
for j in arr:
	s = s + repr(j) + " "
print (s.strip())