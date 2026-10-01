# reducing intervals
# Example : [[1,4],[2,3],[1,5]]
# Output : [[1,5]]
l1 = [[1,4],[2,3],[1,5],[9,11],[10,12]]
for i in range(len(l1)):
    for j in range(len(l1)):
        if i != j:
            if l1[i][0] <= l1[j][1] and l1[j][0] <= l1[i][1]:
                l1[i][0] = min(l1[i][0], l1[j][0])
                l1[i][1] = max(l1[i][1], l1[j][1])
                l1[j] = [-1, -1]
l1 = [interval for interval in l1 if interval != [-1, -1]]
print(l1)