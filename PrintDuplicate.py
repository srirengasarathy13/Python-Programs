
"""
l1 = [1,2,3,4,5,1,2,3,5]

result = []

for i in set(l1):
    if l1.count(i)>1:
        result.append(i)

        
print(result)

"""

l1 = [1,2,3,4,5,1,2,3,5]

result = []

for i in l1:
    if l1.count(i)> 1 and i not in result:
        result.append(i)

        
print(result)