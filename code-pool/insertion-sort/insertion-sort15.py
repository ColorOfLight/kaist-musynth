def ordena(lista):
	g_num = lista[-1]
	for x in range(len(lista)-2,-1,-1):
		if lista[x]>=g_num:
			lista[x+1] = lista[x]	
			
			if x==0:
				lista[0] = g_num
				
		else:
			lista[x+1] = g_num				
			
			break
	return lista


r = int(input())
g_numbers = [int(v) for v in input().split(' ')]
for x in range(0,len(g_numbers)):
	g_numbers[0:x+1] = ordena(g_numbers[0:x+1])

print('%s' % ' '.join(map(str, g_numbers)))