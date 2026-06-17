"""
l1 = [1,2,3,4,5]
if int(input()) in l1:
    print("Element exists !")
else:
    print("Element doesn't exists !")

"""

l1 = [1,2,3,4,5]
n = int(input())
for i in l1:
    if n==i:
        print("Element exists !")
        break
else:
    print("Element doesn't exists !")