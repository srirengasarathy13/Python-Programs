a=[1,2,4,5]
b =[]
for i in a:
    if i in b:
        print(i)
        break
    b.append(i)

else:
    print("No duplicate found!")