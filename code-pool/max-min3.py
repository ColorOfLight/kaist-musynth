N = int(input())
K = int(input())
candy = []

for i in range(N):
    candy.append(int(input()))

candy.sort()
unfair = candy[K-1] - candy[0]

for i in range(N-K+1):
    if unfair > candy[i+K-1] - candy[i]:
        unfair = candy[i+K-1] - candy[i]


print (unfair)