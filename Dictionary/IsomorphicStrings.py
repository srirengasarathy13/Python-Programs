pattern = input("Enter pattern: ")
str1 = input("Enter string to check : ")
words  = str1.split()
stream = {}
for i in range(len(pattern)):
    currentWord, currentSentence = pattern[i], words[i]
    if currentWord in stream and stream[currentWord] != currentSentence:
        print("Not Isomorphic")
        break
    stream[currentWord] = currentSentence
print("Isomorphic")
