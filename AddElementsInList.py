# Method = 1
"""
a = []
n = int(input("Enter the size of the List : "))
for i in range(n):
    a.append(int(input()))
print(a)

"""

# Method 2
"""
n = int(input("Enter the size of the List : "))
a = [0]*n
for i in range(n):
    a[i] = int(input())
print(a)

"""
# Method 3

a = input("Enter the elements : ")
print(a.split(","))
