"""str1 = "Python Is A Programming Language"
vowels = "AEIOUaeiou"
chars = list(str1)
left = 0
right = len(chars) - 1
while left < right:
    while left < right and chars[left] not in vowels:
        left += 1
    while left < right and chars[right] not in vowels:
        right -= 1
    chars[left], chars[right] = chars[right], chars[left]
    left += 1
    right -= 1

result = "".join(chars)
print(result)


"""

str1 = "Python Is A Programming Language"
vowels = "AEIOUaeiou"
capturedVowels = []
str2  = list(str1)
for i in str1:
    if i in vowels:
        capturedVowels.append(i)
answer = []
capturedVowels = capturedVowels[::-1]
n=0
for i in str1:
    if i not in vowels:
        answer.append(i)
    else:
        answer.append(capturedVowels[n])
        n+=1
ans = "".join(answer)
        
print(ans)
