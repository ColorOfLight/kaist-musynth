# Insertion Sort - Part 2
# The method insertionSort takes in one parameter: ar, an unsorted array. Use an Insertion Sort Algorithm to sort the entire array.


#!/bin/python
import sys

# Head ends here
def insertionSort(ar):
	output = ""
	i = 1
	done = False
	ar[0] = int(ar[0])
	while i < len(ar):
		done = False
		toInsert = int(ar.pop(i))
		j = 0
		while j < i and not(done):
			if ar[j] > toInsert:
				ar.insert(j, toInsert);
				done = True
			j += 1
		if(not(done) and j != len(ar)):
			ar.insert(j, toInsert)
		elif(not(done)): 
			ar.append(toInsert)
		i += 1
		
	for val in ar:
		output += str(int(val)) + " "
	output += "\n"

	return output.strip();

# Tail starts here
length = int(sys.stdin.readline())
array = sys.stdin.readline().split(' ')
print(insertionSort(array[0:length]))