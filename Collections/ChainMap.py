from collections import ChainMap


dict1 = {"a":1, "b":1}
dict2 = {"a":2,"c":3}
dict1.update(dict2)
print(dict1)

#-----------------------------------------

default = {"theme": "light", "font": 12}
user = {"theme": "dark"}
ChainMap1 = ChainMap(user, default)
print(ChainMap1)