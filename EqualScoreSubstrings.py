word = 'dbb'
right = left = 0
for i in word:
    right += ord(i) - 96
for i in word:
    value = ord(i) - 96
    left += value
    right -= value
    if left == right:
        print(True)
        quit()
print(False)