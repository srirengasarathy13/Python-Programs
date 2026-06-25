"""
a = "abcde"
b = "deabc"
if len(a) != len(b):
    print("Not a rotation")
else: 
    if b in a+a:
        print("Is a rotation")
    else:
        print("Not a rotation")

"""
str1 = "abcd"
str2 = "cdab"
if len(str1) != len(str2):
    print("Not a rotation")
else:
    for i in range(len(str1)):
        str1 = str1[1:] + str1[0]
        if str1 == str2:
            print("Is a rotation")
            quit()
    print("Not a rotation")