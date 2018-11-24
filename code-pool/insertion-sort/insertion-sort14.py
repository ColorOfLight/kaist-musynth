l = int(input())
ar = input().split()

for size in range(l):
    ar[size] = int(ar[size])

def shift(plist, index):
    temp = plist[index]
    if plist[index-1] > plist[index]:
        plist[index] = plist[index-1]
        plist[index-1] = temp
        if index - 2 == -1:
            pass
        else:
            shift(plist, index-1)
    return plist

for listing in range(1,l):
    string = ''
    ar = shift(ar, listing)

for size2 in range(l):
   string = string + str(ar[size2]) + ' '
print(string)