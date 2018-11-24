import sys

def print_ar(a):
	for i in a:
		print(i, end = ' ');
	print('');

def insert_key(n, ar):
	key = ar[n-1];
	k = n-1;
	for i in range(n-2, -1, -1):
		if key < ar[i]:
			ar[i+1] = ar[i];
			k = k-1;
		else:
			break
	ar[k] = key;

n = int(sys.stdin.readline());
raw = sys.stdin.readline().split();
ar = [];

for i in raw:
	ar.append(int(i));

if n < 2:
	print_ar(ar);
else:
	for i in range(2,n+1):
		insert_key(i, ar);
	print_ar(ar);