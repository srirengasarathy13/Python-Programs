"""
qRow = "qwertyuiop"
aRow = "asdfghjkl"
zRow = "zxcvbnm"
str1 = input("Enter : ").lower()
strList = str1.split(",")
result =[]
for word in strList:
    qCount = 0
    aCount = 0
    zCount = 0
    for i in word:
        if i in qRow:
            qCount+=1
        elif i in aRow:
            aCount+=1
        else:
            zCount+=1
    if aCount == 0 and zCount == 0 :
        result.append(word)    
    elif qCount == 0 and zCount == 0:
        result.append(word) 
    elif qCount == 0 and aCount == 0:
        result.append(word) 
print(result)
"""

#--------------------------------------------------------------------------------------

keyBoard = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
words = ["Hello", "Alaska", "Dad", "Peace", "has"]
result = []
for word in words:
    base = ''
    wordLower = word.lower()
    for i in wordLower:
        if not base:
            for x in keyBoard:
                if i in x:
                    base = x
                    break
        elif i not in base:
            break
    else:
        result.append(word)
print(result)