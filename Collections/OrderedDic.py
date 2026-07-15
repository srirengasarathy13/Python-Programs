from collections import OrderedDict

data = OrderedDict([('b', 2), ('c', 1)])

data.setdefault('a', 5)
data.move_to_end('b')

print(data)

data.popitem(last=False)

print(data)