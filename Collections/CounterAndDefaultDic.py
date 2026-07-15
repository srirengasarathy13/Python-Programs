from collections import defaultdict

str1 = "Hello, World!"
data = defaultdict(int)
for i in str1:
    data[i]+=1
print(data)

