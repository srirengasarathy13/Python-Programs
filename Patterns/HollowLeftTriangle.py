#Program to find the hollow left triangle pattern
n = int(input("Enter the no. of rows : "))
sym = (input("Enter the symbol you want to print : ")).strip()+" "
def hollow_left_triangle(n, sym):
    for i in range(1, n + 1):
        temp = ""
        for j in range(1, i + 1):
            if j == 1 or j == i or i == n:
                temp += sym
            else:
                temp += "  "
        print(temp[:-1])


hollow_left_triangle(n, sym)



