from collections import Counter, defaultdict

str1 = "Hello, World!"
data = defaultdict(int)
for i in str1:
    data[i]+=1
print(data)
counter1 = Counter(str1)
print(counter1)
