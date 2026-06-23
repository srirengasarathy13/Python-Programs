a = "abcde"
b = "deabc"
if len(a) != len(b):
    print("Not a rotation")
else: 
    if b in a+a:
        print("Is a rotation")
    else:
        print("Not a rotation")