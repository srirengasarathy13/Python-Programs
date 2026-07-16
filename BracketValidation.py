"""
# Bracket Validation using Stack

stack = []

brackets = input("Enter brackets: ")

pairs = {'{': '}', '[': ']', '(': ')'}

for i in brackets:
    if i in "{[(":
        stack.append(i)

    elif i in "})]":
        if len(stack) == 0:
            print("Invalid")
            break
        top = stack.pop()
        if pairs[top] != i:
            print("Invalid")
            break
else:
    if len(stack) == 0:
        print("Valid")
    else:
        print("Invalid")

    """

#-----------------------------------------------------------------------------------------------

brackets = '{[()]}'
stack = []
pairs = {'}':'{',']':'[',')':'('}
for i in brackets:
    if i in '{[(':
        stack.append(i)
    elif stack and pairs[i]==stack[-1]:
        stack.pop()
    else:
        print(False)
        quit()
print(False if stack else True)