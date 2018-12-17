n = int(input())
k = int(input())
vals = []
for i in range(n):
    vals.append(int(input()))
vals.sort()
minDiff = vals[-1]
for i in range(n-k+1):
    diff = vals[i+k-1]-vals[i]
    if diff < minDiff:
        minDiff = diff
print(minDiff)