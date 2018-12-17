n = int(input())
k = int(input())
packets=[]

for i in range(n):
    packets.append(int(input()))
    
sortedPack=sorted(packets)

min=sortedPack[k-1] - sortedPack[0]
__HOLE__ = None

print(min)