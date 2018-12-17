n=int(input())
k=int(input())
a=[]
m=0
for i in range(n):
    a.append(int(input()))
a.sort(reverse=True)
m=a[0]-a[k-1]
for i in range(n-k+1):
    if a[i]-a[i+k-1] < m:
        m=a[i]-a[i+k-1]
print(m)