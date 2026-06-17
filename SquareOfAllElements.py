"""
l1 = [1,2,3,4,5]

for i in range(len(l1)):
    l1[i]**=2

print(l1)

"""

"""


l1 = [1,2,3,4,5]

l2 = []

for i in l1:
    l2.append(i**2)

print(l2)


"""

l1 = [1,2,3,4,5]
l2 = [x**2 for x in l1]
print(l2)
