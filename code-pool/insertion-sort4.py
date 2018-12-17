n = int(input())
d = [int(x) for x in input().split()]
i = 1
while i < n:
    k = i
    while k > 0 and d[k] < d[k-1]:
        d[k], d[k-1] = d[k-1], d[k]
        k -= 1
    i += 1

s = str(d)[1:-1].replace(",", "")
print(s)