"""
a="silent"
b="listen"
if sorted(a)==sorted(b):        
    print("The strings are anagrams.")
else:    print("The strings aren't anagrams.") 

"""
"""


a="silent"
b="listen"
for i in a:
    if i not in b or b.count(i)!=a.count(i):
        print("The strings aren't anagrams.")
        break
else:    print("The strings are anagrams.")

"""

"""
str1 = "silent"
str2 = "listen"
str1 = str1.lower()
str2 = str2.lower()
alp = "abcdefghijklmnopqrstuvwxyz"
for i in alp:
    if str1.count(i) != str2.count(i):
        print("The strings aren't anagrams.")
        break
else:    print("The strings are anagrams.")    

"""

str1 = "silent"
str2 = "listen"
alp = [0]*256
for i in str1:
    alp[ord(i)] += 1        
for i in str2:
    alp[ord(i)] -= 1
for i in alp:
    if i != 0:
        print("The strings aren't anagrams.")
        break
else:    print("The strings are anagrams.")