# Program to print the left triangle pattern
n = int(input("Enter the no. of rows : "))
for i in range(1, n + 1):
    temp = ""
    for j in range(1, i + 1):
        temp += "* "
    print(temp[:-1])