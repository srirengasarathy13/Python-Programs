"""
str1 = "Java is a powerful language"
str2 = str1.split()
largest_word = ""
for word in str2:
    if len(word) > len(largest_word):
        largest_word = word
print("Largest word:", largest_word)

"""
"""
str1 = "Java is a powerful language"
longestSize = 0
largest_word = ""
for i in str1.split():
    count = 0
    for char in i:
        count += 1
    if count > longestSize:
        longestSize = count
        largest_word = i
print("Largest word:", largest_word)

"""
"""
str1 = "Java is a powerful language"
largest_word = ""
length = 0
for word in str1.split():
    iLength = len(word)
    if iLength > length:
        length = iLength
        largest_word = word
print("Largest word:", largest_word)

"""
stream = 'Java is a powerful language'
largest = currentLength = 0
result = currentWord = ''
for i in stream+' ':
    if i == ' ':
        if currentLength>largest:
            result = currentWord
            largest = currentLength
        currentWord = ''
        currentLength = 0
    else:
        currentLength += 1
        currentWord += i
print(result)