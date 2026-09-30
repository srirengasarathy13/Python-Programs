s = "aaab"
result = ""
while len(s) > 0:
    found = False
    for i in range(len(s)):
        if len(result) == 0 or s[i] != result[-1]:
            result = result + s[i]
            s = s[:i] + s[i+1:]
            found = True
            break
    if found == False:
        result = ""
        break

print(result)