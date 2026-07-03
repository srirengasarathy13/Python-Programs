# Generate the possible Largest Palindrome from a String
str1 = "aaaabbbcddd"

freq = {}
for ch in str1:
    if ch in freq:
        freq[ch] += 1
    else:
        freq[ch] = 1

left = ""
ones = ""

for i in range(ord('z'), ord('a') - 1, -1):
    ch = chr(i)
    if ch in freq:
        left += ch * (freq[ch] // 2)
        if freq[ch] % 2 == 1 and ones == "":
            ones = ch

palindrome = left + ones + left[::-1]

print(palindrome)



 
