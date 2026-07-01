#Program to find the hollow left triangle pattern
n = int(input("Enter the no. of rows : "))
for i in range(1, n + 1):
    temp = ""
    for j in range(1, i + 1):
        if j == 1 or j == i or i == n:
            temp += "* "
        else:
            temp += "  "
    print(temp[:-1])




