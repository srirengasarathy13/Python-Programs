l1 = [1,2,45,66,7,34,55,89]

max = l1[0]
min = l1[0]

for i in l1 :
    if i>max:
        max = i
    elif i<min:
        min = i    
print(max)
print(min)

