"""
n = int(input("Enter the no. of rows : "))
for i in range(n):
    temp=""
    for j in range(n):
        if i==0 or j==0 or i==n-1 or j==n-1:
            temp+="* "
        else:
            temp+="  "
    print(temp[:-1])

"""
row=int(input("Enter the no. of rows: "))
for i in range(1,row+1):
    if i==1 or i==row:print(('* '*row).strip())
    else:print('* '+'  '*(row-2)+'*')
 