# Program to print the right triangle pattern
def RightTriangle():
    n = int(input("Enter the no. of rows : "))
    for i in range(1, n + 1):
        print("  "*(n - i) + "* " * i)
