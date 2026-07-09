# Program to print the right triangle pattern
n = int(input("Enter the no. of rows : "))
for i in range(n, 0, -1):
    if(i == 1 or i == n):
        print("  "*(n - i) + "* " * i)
    else:
        print("  "*(n - i) + "* " + "  " * (i - 2) + "* ")
