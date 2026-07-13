l1 = [1,2,3,4]
print(list(filter(lambda x: x % 2 == 0, l1)))
print(list(map(lambda x: x ** 2, l1)))

twoDList=[[1,2,3],[4,5,6],[7,8,9]]
print(list(zip(*twoDList)))

print(any([x%2 == 0 for x in l1]))
print(all([x%2 == 0 for x in l1]))
