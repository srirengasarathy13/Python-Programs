# Program to print the right triangle pattern with return type
def right_inverted_triangle(n):
    result = ""
    for i in range(n, 0, -1):
        if(i == 1 or i == n):
            result += "  "*(n - i) + "* " * i + "\n"
        else:
            result += "  "*(n - i) + "* " + "  " * (i - 2) + "* \n"
    return result.strip()
            
n=int(input("Enter the number of rows: "))
print(right_inverted_triangle(n))