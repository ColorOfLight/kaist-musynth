n = int(input())
k = int(input())

arr =[]

for i in range(n):
    x = int(input())
    arr.append(x);
    
arr.sort()

mn = arr[k-1] - arr[0] 
for i in range(n-k):
    mn = min(arr[k+i] - arr[i+1], mn)
    
print(mn)