# Hollow Left Inverted Triangle Pattern
n = int(input("Enter the number of rows: "))
for i in range(n, 0, -1):
    for j in range(1, n + 1):
        if j == 1 or j == i or i == n:
            print("* ", end=" ")
        else:
            print("  ", end=" ")
    print()