def calculate(s):
    nums = []
    ops = []
    i = 0
    while i < len(s):
        if s[i].isdigit():
            nums.append(int(s[i]))
        elif s[i] in "+-*/":
            ops.append(s[i])
        elif s[i] == '(':
            start = i + 1
            count = 1
            i += 1
            while count != 0:
                if s[i] == '(':
                    count += 1
                elif s[i] == ')':
                    count -= 1
                i += 1
            result = calculate(s[start:i-1])
            nums.append(result)
            continue
        i += 1
    result = nums[0]
    for i in range(len(ops)):
        if ops[i] == '+':
            result += nums[i + 1]
        elif ops[i] == '-':
            result -= nums[i + 1]
        elif ops[i] == '*':
            result *= nums[i + 1]
        elif ops[i] == '/':
            result //= nums[i + 1]
    return result
print(calculate("3-2*4"))
