#Count Frequency of each word in a string
#aaaabbbcddd

str1 = "aaaabbbcddd"
freq = {}
for i in str1:
    if i in freq:
        freq[i] += 1
    else:
        freq[i] = 1
print(freq)