def insertionSort(x):
    p=len(x)-1
    for k in range(p):
        y=x[-1]
        if y<x[-2]:
            for i in range(p, 0, -1):   
                if x[i-1]>=y:
                    x[i]=x[i-1] 
                else:
                    x[i]=y  
                    break
                 
    
            if x[0]>=x[1]:
                x[0]=y
        else: 
            break
    return x

def insertionSort2(x):
    l=len(x)
    m=[x[0]]
    s=[]
    for i in range(1, l):
        m.append(x[i])
        if x[i]<x[i-1]:
            insertionSort(m)
        x=m+x[i+1:]
    return x

m = input()
ar = [int(i) for i in input().strip().split()]
ar = insertionSort2(ar)
print(" ".join( str(j) for j in ar))