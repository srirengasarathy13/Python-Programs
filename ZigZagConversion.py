str1 = 'PAYPALISHIRING'
rows = 4
stream = ['']*rows
index = rev = 0
for x in str1:
    stream[index] += x
    if index == 0:
        rev = 0
    elif index == rows - 1:
        rev = 1
    index += -1 if rev else 1
print(''.join(stream))