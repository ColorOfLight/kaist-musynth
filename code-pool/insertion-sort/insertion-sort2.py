n = int(input())
line = list(map(int, input().split()))

def  list_print(lst):
    print( ' '.join(map(str, lst) ) )

def insert(lst, i):
    """Insert element at ith position into sublist [0, i] inplace"""
    pos = i-1
    for pos in range(i-1, -1, -1):
        if lst[pos] > lst[pos+1]:
            lst[pos], lst[pos+1] = lst[pos+1], lst[pos]
                    
    
for stop in range(1, n):
    insert(line, stop)

list_print(line)