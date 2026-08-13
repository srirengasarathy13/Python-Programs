# Program to print the pyramid pattern
num = int(input("Enter the no. of rows : "))
for i in range(num):
    print("  "*(num-i-1) + "* " * (2*i+1))