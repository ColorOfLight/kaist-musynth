#!/usr/bin/env python3
import sys

count = None
a_list = None

for line in sys.stdin:
    if count is None:
        count = int(line.strip())
        continue
    a_list = [int(i) for i in line.strip().split(' ')]

for i in range(1, count):
    V = a_list[i]
    for j in range(i):
        if V < a_list[i - j - 1]:
            tmp = a_list[i - j - 1]
            a_list[i - j - 1] = V
            a_list[i - j] = tmp

print(' '.join([str(x) for x in a_list]))