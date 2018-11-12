numbers=int(input('numbers?').split())
length=len(numbers)

def q_sort(num_list):
    if len(num_list)==1:
        return num_list
    pivot=num_list[0]
    list1=[]
    list2=[]
    for i in range(1,len(num_list)):
        #Hole: sort // numbers

        '''if num_list[i]<=pivot:
            list1.append(num_list[i])
        else:
            list2.append(num_list[i])'''
    return(q_sort(list1)+[pivot]+q_sort(list2))
q_sort(numbers)

print(numbers[-1])
