"""
a = "swiss"
for i in a:
    if a.count(i) == 1:
        print(i)
        break

"""

a = "swiss"
count = [0]*26
for i in a:
    count[ord(i)-97] += 1
for i in a:
    if count[ord(i)-97] == 1:
        print(i)
        break