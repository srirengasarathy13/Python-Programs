words = ["car", "god", "one"]
rows = len(words)
cols = len(words[0])
result = []
for d in range(rows + cols - 1):
    temp = ""
    for i in range(rows):
        j = d - i
        if 0 <= j < cols:
            temp += words[i][j] 
    result.append(temp)
for i in range(len(result)):
    if i%2!=0:
        result[i] = result[i][::-1]
print(result) 