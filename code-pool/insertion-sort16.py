def sort(li, i):
    j = i-1
    while j >= 0:
        if li[j] <= li[i]:
            break
        help = li[i]
        li[i] = li[j]
        li[j] = help
        i-=1
        j-=1
    
n = int(input())
array = [int(x) for x in input().split()]
for i in range(1, n):
    sort(array, i)
print(' '.join(map(str, array)))