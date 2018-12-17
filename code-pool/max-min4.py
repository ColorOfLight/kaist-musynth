n = int(input())
k = int(input())
a = []
for i in range(n):
    a.append(int(input()))
    
a = sorted(a)
minimum = a[k - 1] - a[0]
for i in range(n - k + 1):
    if a[i + k - 1] - a[i] < minimum:
        minimum = a[i + k - 1] - a[i]
        
print(minimum)