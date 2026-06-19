"""
a="silent"
b="listen"
if sorted(a)==sorted(b):        
    print("The strings are anagrams.")
else:    print("The strings aren't anagrams.") 

"""


a="silent"
b="listen"
for i in a:
    if i not in b or b.count(i)!=a.count(i):
        print("The strings aren't anagrams.")
        break
else:    print("The strings are anagrams.")


