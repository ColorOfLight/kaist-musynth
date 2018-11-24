import sys
# Puts a the last element in the array in the back inthe an already sorted array
def insert(ar):    
    e = int(len(ar)) - 1
    newNum = ar[e]
    done = False
    while done == False:
        if ar[e-1] > newNum:
            ar[e] = ar[e-1]
            e-=1
            done = e == 0
        else:
            done = True      
    ar[e] = newNum
    
    return ar
def insertionSort(ar):
    if(len(ar)>1):
        for i in range(1,len(ar)):
            if ar[i-1] > ar[i]:
                ar[0:i+1]=insert(ar[0:i+1])
    return ar

def buildString(ar):
    string = str(" ")
    for i in range(len(ar)):
        string += str(ar[i]) + " "
    sys.stdout.write(string.strip()+'\n')
    return string

def raw_input():
    m = input()
    return m

# Tail starts here

    
def main():
    m = int(input())
    i = int(0)
    ar = list()
   # while i < m:
    #    ar.append( raw_input() )
     #   i+=1
    ar = [int(i) for i in raw_input().strip().split()]
    insertionSort(ar)
    buildString(ar)
    return 0
if __name__ == '__main__':
    main()