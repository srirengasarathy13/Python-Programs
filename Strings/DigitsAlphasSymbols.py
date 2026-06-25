str1="Java@123"
result = [0,0,0]
for i in str1:
    if i.isdigit():
        result[0] += 1
    elif i.isalpha():
        result[1] += 1
    else:
        result[2] += 1
print("Digits:", result[0])
print("Alphabets:", result[1])
print("Symbols:", result[2])

