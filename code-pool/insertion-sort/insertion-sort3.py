s = int(input())
input_ar = input().split()
ar = [int(x) for x in input_ar]

for i in range(1, s):
    j = i - 1
    # no need to move
    if ar[i] >= ar[j]:
        continue
    # otherwise, insert into the sorted part
    v = ar[i]
    while v < ar[j] and j >= 0:
        ar[j + 1] = ar[j]
        j -= 1
    # insert v
    ar[j + 1] = v

print(' '.join([str(x) for x in ar]))