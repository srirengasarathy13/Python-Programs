#Compress a String. (Example : aaabbcccc , a3b2c4)

"""
text = input("Enter a string to compress: ")

compressed = ""
count = 1

for i in range(1, len(text)):
    if text[i] == text[i - 1]:
        count += 1
    else:
        compressed += text[i - 1] + str(count)
        count = 1

if text:
    compressed += text[-1] + str(count)

print(compressed)  

"""

stri = input("Enter a string to compress: ")
alp = [0]*26
compressed = ""
for i in stri:
    alp[ord(i)-97] += 1
    
for i in range(26):
    if alp[i] > 0:
        compressed += chr(i+97) + str(alp[i])
print(compressed)