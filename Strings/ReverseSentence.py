"""
sentence = "Java is awesome"
reversed_sentence = ""
for word in sentence.split():
    reversed_sentence = word + " " + reversed_sentence
print("Reversed sentence:", reversed_sentence)
"""
str1 = 'Java is awesome'
result = currentString =  ''
for i in str1+' ':
    if i == ' ':
        result = ' '+currentString+result
        currentString= ''
    else:
        currentString+=i
print(result[1:])