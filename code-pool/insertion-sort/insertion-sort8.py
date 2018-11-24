#!/bin/python3

# Head ends here
def insert(ar):
    u = ar.pop()
    for i in range(len(ar)):
        if ar[i] >= u: ar.insert(i,u);return ar
    ar.append(u)
    return ar

def insertionSort(ar):
    for i in range(2,len(ar)+1):
        ar[0:i] = insert(ar[0:i])

    print(' '.join([str(i) for i in ar]))

# Tail starts here

m = int(input())
ar = [int(i) for i in input().strip().split()]
if m == 1:
    print(' '.join([str(i) for i in ar]))
elif m == len(ar):
    insertionSort(ar)