words = ["eat", "tea", "tan", "ate", "nat", "bat"]

dict = {}

for word in words:
    key = "".join(sorted(word))

    if key in dict:
        dict[key].append(word)
    else:
        dict[key] = [word]

print(dict)