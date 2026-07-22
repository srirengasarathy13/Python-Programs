list =[1,5,8,5,9] 
result=[]
for i in range(len(list)):
    temp=1
    for j in range(len(list)):
        if(i!=j):
            temp=temp*list[j]
    result.append(temp)
print(result)