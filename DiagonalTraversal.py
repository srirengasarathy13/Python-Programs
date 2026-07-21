words = ["car", "god", "one","python"]
rows = len(words)
cols = max(len(word) for word in words)
result = []
for d in range(rows + cols - 1):
    temp = ""
    for i in range(rows):
        j = d - i
        if 0 <= j < len(words[i]):
            temp += words[i][j]
        elif 0 <= j < cols:
            temp+=" "            
    result.append(temp)
for i in range(len(result)):
    if i%2!=0:
        result[i] = result[i][::-1]
print(result) 