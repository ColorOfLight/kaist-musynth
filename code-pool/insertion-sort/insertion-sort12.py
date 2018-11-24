x = int(input())
a = input().split()

if(x==1):
    print(a[0])

j = 1
while(j<x):
    i = j
    v = int(a[i])
    while(i>0):
        t1 = int(a[i-1])
        if(t1>v):
            a[i] = t1
            a[i-1] = v
        i-=1
    j+=1

for num in a:
    print(num, end=' ')
print()