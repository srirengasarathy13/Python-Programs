# Grouping
dict1 = {"John": 20, "Mary": 21, "Tom": 20, "Alice": 21}
grououped_dict = {}
for i in dict1:
    if dict1[i] in grououped_dict:
        grououped_dict[dict1[i]].append(i)
    else:
        grououped_dict[dict1[i]] = [i]
print(grououped_dict)