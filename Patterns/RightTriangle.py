# Program to print the right triangle pattern
n = int(input("Enter the no. of rows : "))
for i in range(1, n + 1):
    print("  "*(n - i) + "* " * i)
