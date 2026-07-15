from collections import deque

data = deque([1, 3, 2, 5])

data.rotate(3)
print(data)

data.appendleft(6)
data.extendleft([8, 9])
print(data)

print(data.pop())
print(data.popleft())

data.extend([10, 11])
print(data)