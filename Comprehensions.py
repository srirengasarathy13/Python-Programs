# List
# print([x for x in range(1,5)])   

# Dictionary
# print({x:chr(x+97) for x in range(26)})   

# Set
# print({x for x in 'abbacd'})   #Set


# Generators
# stream = (x for x in range(1,5))
# for i in stream:
#     print(i)

print(['odd' if x%2 else 'even' for x in range(1,5)])

print([x for x in range(1,5) if x%2])

def sample(x):
    if x==1:
        return 'One'
    elif x==2:
        return 'Two'
    elif x==3:
        return 'Three'
print([sample(x) for x in range(1,5)])