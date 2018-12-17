n = int(input())
k = int(input())
packets=[]

for i in range(n):
    packets.append(int(input()))
    
sortedPack=sorted(packets)

min=sortedPack[k-1] - sortedPack[0]
for i in range(n-k):
    __HOLE__ = None
    if temp<min:
        min=temp
print(min)